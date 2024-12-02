from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 12, 3),
    'retries': 1,
}

dag = DAG(
    'sparl my dag',
    default_args=default_args,
    description='dag example',
    schedule_interval='@daily',
)

spark_submit_task = SparkSubmitOperator(
    task_id='run_spark_job',
    application='../src/main.py',
    conn_id='spark_default',
    dag=dag,
)

spark_submit_task.dry_run()

