from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from source.utils import helpers

DAG_ID = "example_Postgres"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    pg_test_task = PostgresOperator(
        task_id="postgres_test",
        postgres_conn_id='postgres_connid',
        sql=helpers.load_query_template("datawarehouse/example.sql"),
    )

    pg_test_task
