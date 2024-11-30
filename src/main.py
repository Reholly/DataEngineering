from pyspark.sql import SparkSession

from config import POSTGRES_DSN, DB_PASSWORD, DB_USER, MINIO_ADDR, S3_ADMIN, S3_PASSWORD
from load_news_data import MinioDataLoader
from src.transform_data_mart import transform_data_mart
from transform_market_data import transform_market_data
from transform_news_data import transform_news
from load_market_data import load_market_data

def main():
    spark_session = SparkSession \
        .builder \
        .master("spark://localhost:7077") \
        .config("spark.jars", "/home/evgenii/PycharmProjects/DataEngineering/spark/jars/postgresql-42.7.4.jar") \
        .getOrCreate()
    properties = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "driver": "org.postgresql.Driver"
    }

    raw_market_data = load_market_data(POSTGRES_DSN, spark_session, properties)
    raw_news_data = MinioDataLoader().load_data_from_s3(MINIO_ADDR, S3_ADMIN, S3_PASSWORD)

    transformed__news_data = transform_news(raw_news_data, spark_session)
    transformed_market_data = transform_market_data(raw_market_data)

    transformed__news_data.Events.show()
    transformed__news_data.Locations.show()
    transformed__news_data.Categories.show()

    transformed_market_data.Stocks.show()
    transformed_market_data.Candles.show()
    print(transformed__news_data.Events, transformed__news_data.Locations, transformed__news_data.Categories)
    print(transformed_market_data.Stocks,transformed_market_data.Candles)

    transform_data_mart(spark_session, transformed_market_data, transformed__news_data)

if __name__ == "__main__":
    main()
