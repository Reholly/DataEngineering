from pyspark import Row
from pyspark.sql import SparkSession

from transformed_data import MarketData, NewsData
from pyspark.sql import functions as F
from pyspark.sql.functions import sum, col


def transform_data_mart(spark: SparkSession, market_data: MarketData, news_data: NewsData):
    # Проходимся по каждому событию
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



        # Получаем уникальные значения в колонне 'category'
        unique_tickers_weekly = weekly_filtered.select("stock_ticker").distinct().rdd.flatMap(lambda x: x).collect()
        unique_tickers_monthly = monthly_filtered.select("stock_ticker").distinct().rdd.flatMap(lambda x: x).collect()

        weekly_ticker_stocks = []
        monthly_ticker_stocks = []

        # Создаем отдельные DataFrame для каждого уникального значения
        for ticker in unique_tickers_weekly:
            weekly_ticker_stocks.append(weekly_filtered.filter(weekly_filtered.stock_ticker == ticker))

        for ticker in unique_tickers_monthly:
            monthly_ticker_stocks.append(monthly_filtered.filter(monthly_filtered.stock_ticker == ticker))

        for stock in weekly_ticker_stocks:




        weekly_changes = weekly_filtered.agg(sum("price_change").alias("final_all_cost_change")).first()[0]
        monthly_changes = monthly_filtered.agg(sum("price_change").alias("final_all_cost_change")).first()[0]

        initial_price_weekly = weekly_filtered.select(F.first("open_cost").alias("initial_price")).first()[0]
        initial_price_monthly = weekly_filtered.select(F.first("open_cost").alias("initial_price")).first()[0]

        percentage_change_weekly = (weekly_changes / initial_price_weekly) * 100
        percentage_change_monthly = (monthly_changes / initial_price_monthly) * 100

        num_days_weekly = weekly_filtered.count()
        num_days_monthly = monthly_filtered.count()

        speed_change_weekly = weekly_changes / num_days_weekly if num_days_weekly > 0 else None
        speed_change_monthly = monthly_changes / num_days_monthly if num_days_monthly > 0 else None

        result_data_weekly = Row(
                           initial_cost = initial_price_weekly,
                           total_change=weekly_changes,
                           percentage_change=percentage_change_weekly,
                           speed_change=speed_change_weekly)

        result_data_monthly = Row(
                           initial_cost=initial_price_weekly,
                           total_change=monthly_changes,
                           percentage_change=percentage_change_monthly,
                           speed_change=speed_change_monthly)

        result_df = spark.createDataFrame([result_data_weekly, result_data_monthly])

        print(result_df)
        result_df.show()
