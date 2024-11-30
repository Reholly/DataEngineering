from pyspark.sql.connect.dataframe import DataFrame
from pyspark.sql.connect.session import SparkSession

from config import CH_USER, CH_HOST
from config import CH_DB_NAME, CH_PASSWORD, CH_PORT
from transformed_data import MarketData
from transformed_data import NewsData


def load_result_data_to_clickhouse(spark: SparkSession, result_df: DataFrame, news_data: NewsData, market_data: MarketData):
    clickhouse_url = f"jdbc:clickhouse://{CH_HOST+":"+CH_PORT}:{CH_PASSWORD}/{CH_DB_NAME}"
    table_name = "data_mart_fact"

    clickhouse_options = {
        "url": f"jdbc:clickhouse://{CH_HOST+":"+CH_PORT}:{CH_PASSWORD}/{CH_DB_NAME}",
        "user": CH_USER,
        "password": CH_PASSWORD,
        "dbtable": table_name,
        "driver": "com.clickhouse.jdbc.Driver"
    }

    result_df.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", table_name) \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
             .save()

    news_data.Events.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "event") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()

    news_data.Locations.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "location") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()

    news_data.Categories.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "category") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()

    news_data.EventPerCategoryLink.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "categories_per_event") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()

    news_data.EventPerLocationLink.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "categories_per_location") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()

    market_data.Stocks.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "stock") \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .option("driver", "com.clickhouse.jdbc.Driver") \
        .mode("append") \
        .save()
