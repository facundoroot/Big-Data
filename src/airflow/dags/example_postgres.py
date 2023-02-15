from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

DAG_ID = "postgres_operator_dag"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:
    pg_test_task = PostgresOperator(
        task_id="postgres_test",
        postgres_conn_id='postgres_connid',
        sql="""
            SELECT * FROM public.employee;
        """,
    )

    pg_test_task
