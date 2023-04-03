from airflow import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


dag = DAG(
    'example_mongodb',
    description='Hello World DAG',
    schedule_interval='0 12 * * *',
    start_date=datetime(2017, 3, 20), catchup=False
)


def query_mongodb():
    mongo_hook = MongoHook(conn_id='mongodb_connid')
    client = mongo_hook.get_conn()
    sample_db = client.sample_db
    sample_collection = sample_db.sample_collection
    documents = sample_collection.find()
    print(documents)
    for document in documents:
        print(document)


mongo_task = PythonOperator(
    task_id='mongodb_query_task',
    python_callable=query_mongodb,
    dag=dag
)

mongo_task
