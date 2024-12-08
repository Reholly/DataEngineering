import datetime
import sys

from airflow.decorators import dag
from airflow.utils.dates import days_ago
from main import main

sys.path.append("..")


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

@dag(
    dag_id="main_dag",
    description="main dag for all",
    default_args=default_args,
    start_date=datetime.datetime.today(),
    schedule="@daily",
    catchup=False,
)
def run_main_script():
   main()

dag = run_main_script()