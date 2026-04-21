from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys

default_args = {
    'owner': 'ayush',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_etl():
    subprocess.run([sys.executable, '/opt/airflow/etl/etl_pipeline.py'], check=True)

def run_seed():
    subprocess.run([sys.executable, '/opt/airflow/etl/seed.py'], check=True)

with DAG(
    dag_id='real_estate_crm_etl',
    default_args=default_args,
    description='Real Estate CRM ETL Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 4, 1),
    catchup=False,
    tags=['real-estate', 'etl']
) as dag:

    seed_task = PythonOperator(
        task_id='seed_database',
        python_callable=run_seed
    )

    etl_task = PythonOperator(
        task_id='run_etl_pipeline',
        python_callable=run_etl
    )

    seed_task >> etl_task