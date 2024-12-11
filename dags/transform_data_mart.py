from pyspark import Row
from pyspark.sql import SparkSession, DataFrame

from transformed_data import MarketData, NewsData
from pyspark.sql import functions as F
from pyspark.sql.functions import sum, col
from datetime import datetime, timedelta


def transform_data_mart(spark: SparkSession, market_data: MarketData, news_data: NewsData) -> DataFrame:
    result_df = spark.createDataFrame([Row(event_id="",
                stock_ticker="ticker",
                main_theme="INITIAL SCHEMA",
                change_cost_start_date=datetime.now(),
                change_cost_end_date= datetime.now(),
                initial_cost="",
                total_change="",
                percentage_change="",
                speed_change="")])
    for row in news_data.Events.collect():

        event_time = row.appearance_date

        one_week_further = event_time + F.expr("INTERVAL 7 DAYS")
        one_month_further = event_time + F.expr("INTERVAL 30 DAYS")

        weekly_filtered = market_data.Candles.filter(
            (market_data.Candles.time <= one_week_further) & (market_data.Candles.time >= event_time))
        monthly_filtered = market_data.Candles.filter(
            (market_data.Candles.time <= one_month_further) & (market_data.Candles.time >= event_time))

        weekly_filtered = weekly_filtered.withColumn("price_change", col("close_cost") - col("open_cost"))
        monthly_filtered = monthly_filtered.withColumn("price_change", col("close_cost") - col("open_cost"))

        unique_tickers_weekly = weekly_filtered.select("stock_ticker").distinct().rdd.flatMap(lambda x: x).collect()
        unique_tickers_monthly = monthly_filtered.select("stock_ticker").distinct().rdd.flatMap(lambda x: x).collect()

        weekly_ticker_stocks = []
        monthly_ticker_stocks = []

        for ticker in unique_tickers_weekly:
            weekly_ticker_stocks.append(weekly_filtered.filter(weekly_filtered.stock_ticker == ticker))

        for ticker in unique_tickers_monthly:
            monthly_ticker_stocks.append(monthly_filtered.filter(monthly_filtered.stock_ticker == ticker))

        for stocks in weekly_ticker_stocks:
            ticker = stocks.select(F.first("stock_ticker")).first()[0]
            event_id = row.uuid

            weekly_changes = stocks.agg(sum("price_change").alias("final_all_cost_change")).first()[0]
            initial_price_weekly = stocks.select(F.first("open_cost").alias("initial_price")).first()[0]
            percentage_change_monthly = (weekly_changes / initial_price_weekly) * 100
            num_days_monthly = stocks.count()
            speed_change_monthly = weekly_changes / num_days_monthly if num_days_monthly > 0 else None
            result_data_weekly = Row(
                event_id=event_id,
                stock_ticker=ticker,
                main_theme=row.title,
                change_cost_start_date=event_time,
                change_cost_end_date=event_time + timedelta(weeks=1),
                initial_cost=initial_price_weekly,
                total_change=weekly_changes,
                percentage_change=percentage_change_monthly,
                speed_change=speed_change_monthly)
            new_df = spark.createDataFrame([result_data_weekly])
            result_df = result_df.union(new_df)

        for stocks in monthly_ticker_stocks:
            ticker = stocks.select(F.first("stock_ticker")).first()[0]
            event_id = row.uuid

            monthly_changes = stocks.agg(sum("price_change").alias("final_all_cost_change")).first()[0]
            initial_price_monthly = stocks.select(F.first("open_cost").alias("initial_price")).first()[0]
            percentage_change_monthly = (monthly_changes / initial_price_monthly) * 100
            num_days_monthly = stocks.count()
            speed_change_monthly = monthly_changes / num_days_monthly if num_days_monthly > 0 else None
            result_data_monthly = Row(
                event_id=event_id,
                stock_ticker=ticker,
                main_theme=row.title,
                change_cost_start_date=event_time,
                change_cost_end_date=event_time + timedelta(weeks=4),

                initial_cost=initial_price_monthly,
                total_change=monthly_changes,
                percentage_change=percentage_change_monthly,
                speed_change=speed_change_monthly)
            new_df = spark.createDataFrame([result_data_monthly])
            result_df = result_df.union(new_df)

    return result_df