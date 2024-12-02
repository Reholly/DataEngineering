from pyspark.sql import SparkSession
from config import POSTGRES_DSN, DB_PASSWORD, DB_USER, MINIO_ADDR, S3_ADMIN, S3_PASSWORD
from load_to_clickhouse import load_to_clickhouse
from src.extract_news_data import load_data_from_s3
from transform_data_mart import transform_data_mart
from transform_market_data import transform_market_data
from transform_news_data import transform_news
from extract_market_data import load_market_data

def main():
    jar_files = "../spark/jars/postgresql-42.7.4.jar, ../spark/jars/clickhouse-jdbc-0.7.0.jar,../spark/jars/clickhouse-spark-runtime-3.4_2.12-0.7.3.jar,../spark/jars/httpclient5-5.4.jar"
    spark_session = (SparkSession
        .builder
        .master("spark://localhost:7077")
        .config("spark.jars", jar_files)
        .getOrCreate())
    properties = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "driver": "org.postgresql.Driver"
    }

    raw_market_data = load_market_data(POSTGRES_DSN, spark_session, properties)
    raw_news_data = load_data_from_s3(MINIO_ADDR, S3_ADMIN, S3_PASSWORD)

    transformed_news_data = transform_news(raw_news_data, spark_session)
    transformed_market_data = transform_market_data(raw_market_data)

    result_df = transform_data_mart(spark_session, transformed_market_data, transformed_news_data)

    load_to_clickhouse(result_df, transformed_news_data, transformed_market_data)
    spark_session.stop()

if __name__ == "__main__":
    main()
