from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from project.tools.utils.helpers import load_query_template

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
        sql=load_query_template("airflow_queries/postgres/example.sql"),
    )

    pg_test_task
