from pyspark.sql import SparkSession

from config import POSTGRES_DSN, DB_PASSWORD, DB_USER, MINIO_ADDR, S3_ADMIN, S3_PASSWORD
from load_news_data import MinioDataLoader
from transform_market_data import transform_market_data
from transform_news_data import transform_news
from load_market_data import load_market_data

def main():
    spark_session = SparkSession \
        .builder \
        .appName("Data Engineering CSU project") \
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

    print(transformed__news_data)
    print(transformed_market_data)

if __name__ == "__main__":
    main()
