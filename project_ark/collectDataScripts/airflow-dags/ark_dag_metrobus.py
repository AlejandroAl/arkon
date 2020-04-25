from datetime import timedelta
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src import DataCdmxScripts 
from src import ShapesPoints


default_args = {
    'owner': 'arkon_data',
    'start_date': datetime(2020, 4, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'arkon_data_metrobus_townhall',
    default_args=default_args,
    catchup=False,
    description='A simple tutorial DAG',
    schedule_interval="@hourly",
)


metrobus = PythonOperator(
    task_id="metrobus",
    python_callable=DataCdmxScripts.getDataMetrobus,
    dag=dag
)

addTownHall = PythonOperator(
    task_id="addTownHall",
    python_callable=ShapesPoints.addTownHall,
    dag=dag
)

metrobus >> addTownHall