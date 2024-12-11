from airflow import DAG
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from datetime import datetime

from config import POSTGRES_DSN, MINIO_ADDR, S3_ADMIN, S3_PASSWORD, DB_USER, DB_PASSWORD
from transform_market_data import transform_market_data
from transform_news_data import transform_news
from extract_news_data import load_data_from_s3
from extract_market_data import load_market_data


def create_spark_session():
    jar_files = "/opt/airflow/spark/jars/postgresql-42.7.4.jar, /opt/airflow/spark/jars/clickhouse-jdbc-0.7.0.jar,/opt/airflow/spark/jars/clickhouse-spark-runtime-3.4_2.12-0.7.3.jar, /opt/airflow/spark/jars/httpclient5-5.4.jar"
    return (SparkSession
                     .builder
                     .master("spark://spark-master:7077")
                     .config("spark.jars", jar_files)
                     .getOrCreate())

def extract_market_data(session: SparkSession):
    properties = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "driver": "org.postgresql.Driver"
    }
    return load_market_data(POSTGRES_DSN, session, properties)

def extract_news_data():
   return load_data_from_s3(MINIO_ADDR, S3_ADMIN, S3_PASSWORD)

def transform_news_data(raw_news_data, session):
    return transform_news(raw_news_data, session)

def transform_market_data_from_s3(raw_market_data):
    return transform_market_data(raw_market_data)

def transform_data_mart(session: SparkSession, transformed_market_data, transformed_news_data):
    return transform_data_mart(session, transformed_market_data, transformed_news_data)

def load_to_clickhouse(result_df, transformed_news_data, transformed_market_data):
    return load_to_clickhouse(result_df, transformed_news_data, transformed_market_data)

# DAG по умолчанию
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 11),
    'retries': 1,
}

dag = DAG(
    'market_news_data_pipeline',
    default_args=default_args,
    description='DAG for processing market and news data',
    schedule_interval='@daily',
)


sp_session = create_spark_session()
load_market_data_task = PythonOperator(
    task_id='extract_market_data',
    python_callable=extract_market_data,
    op_kwargs={'session': sp_session},
    dag=dag,
)

load_data_from_s3_task = PythonOperator(
    task_id='extract_data_from_s3',
    python_callable=extract_news_data,
    op_kwargs={},
    dag=dag,
)

transform_news_task = PythonOperator(
    task_id='transform_news',
    python_callable=transform_news_data,
    op_kwargs={'raw_news_data': '{{ task_instance.xcom_pull(task_ids="load_data_from_s3") }}', 'session': sp_session},
    dag=dag,
)

transform_market_data_task = PythonOperator(
    task_id='transform_market_data',
    python_callable=transform_market_data_from_s3,
    op_kwargs={'raw_market_data': '{{ task_instance.xcom_pull(task_ids="load_market_data") }}'},
    dag=dag,
)

transform_data_mart_task = PythonOperator(
    task_id='transform_data_mart',
    python_callable=transform_data_mart,
    op_kwargs={
        'session': sp_session,
        'transformed_market_data': '{{ task_instance.xcom_pull(task_ids="transform_market_data") }}',
        'transformed_news_data': '{{ task_instance.xcom_pull(task_ids="transform_news") }}'
    },
    dag=dag,
)

load_to_clickhouse_task = PythonOperator(
    task_id='load_to_clickhouse',
    python_callable=load_to_clickhouse,
    op_kwargs={
        'result_df': '{{ task_instance.xcom_pull(task_ids="transform_data_mart") }}',
        'transformed_news_data': '{{ task_instance.xcom_pull(task_ids="transform_news") }}',
        'transformed_market_data': '{{ task_instance.xcom_pull(task_ids="transform_market_data") }}',
    },
    dag=dag,
)

# Определение зависимостей
load_market_data_task >> load_data_from_s3_task >> [transform_news_task, transform_market_data_task]
transform_market_data_task >> transform_data_mart_task
transform_news_task >> transform_data_mart_task
transform_data_mart_task >> load_to_clickhouse_task
