from pyspark.shell import spark
from pyspark.sql import SparkSession

from config.config import POSTGRES_DSN, DB_PASSWORD, DB_USER, MINIO_ADDR, S3_ADMIN, S3_PASSWORD
from extract.postgres_data_loader import PostgresDataLoader
from extract.minio_data_loader import MinioDataLoader
from transform.news_data_transformer import NewsDataTransformer
from transform.market_data_transformer import MarketDataTransformer


def main():
    spark_session = (SparkSession.builder \
        .appName("TEST") \
        .master("spark://spark-master:7077") \
        .config("spark.jars", "/opt/spark/jars/postgresql-42.7.4.jar") \
        .getOrCreate())
    properties = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "driver": "org.postgresql.Driver"
    }

    postgres_data = PostgresDataLoader().load_from_db(POSTGRES_DSN, spark_session, properties)
    minio_data_loader = MinioDataLoader()
    news_data = minio_data_loader.load_data_from_s3(MINIO_ADDR, S3_ADMIN, S3_PASSWORD)

    print(postgres_data)

    transformed_market_data = MarketDataTransformer().transform(postgres_data)
    print(transformed_market_data)
    transformed_news_data = NewsDataTransformer().transform(news_data, spark)
    print(transformed_news_data)
    spark_session.stop()

if __name__ == "__main__":
    main()
