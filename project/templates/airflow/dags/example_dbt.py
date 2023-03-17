"""Sample basic DAG which dbt runs a project."""
import datetime as dt

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow_dbt_python.operators.dbt import DbtRunOperator

with DAG(
    dag_id="example_dbt",
    schedule_interval="0 * * * *",
    start_date=days_ago(1),
    catchup=False,
    dagrun_timeout=dt.timedelta(minutes=60),
) as dag:
    dbt_run = DbtRunOperator(
        task_id="dbt_run_hourly",
        project_dir="/opt/dbt/",
        profiles_dir="/opt/dbt/",
        models=["my_first_dbt_model"],
        full_refresh=False,
    )
