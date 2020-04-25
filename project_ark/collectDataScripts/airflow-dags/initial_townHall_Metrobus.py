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
    'arkon_data_intialProcess',
    default_args=default_args,
    catchup=False,
    description='Get date first time from CDMX alcandias, Metrobus',
    schedule_interval="@once",
)


metrobus = PythonOperator(
    task_id="metrobus",
    python_callable=DataCdmxScripts.getDataMetrobus,
    dag=dag
)

townHallData = PythonOperator(
    task_id="townHallData",
    python_callable=DataCdmxScripts.getDataTownHall,
    dag=dag
)

addTownHall = PythonOperator(
    task_id="addTownHall",
    python_callable=ShapesPoints.addTownHall,
    dag=dag
)

metrobus >> addTownHall

townHallData >> addTownHall