import os
from datetime import datetime, timedelta
from airflow import DAG

from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.papermill_operator import PapermillOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils import dates

from alphavantage_plugin.operators.alphavantage_to_pg_operator import AlphavantageToPgOperator


default_args = {
    'owner': 'natasha',
    'depends_on_past': False,
    'start_date': dates.days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    dag_id='daily_exchange_rates',
    default_args=default_args,
    description='Extract, load, and transform exchange rate data from Alphavantage to Jupyter via Postgres',
    schedule_interval='0 12 * * *'
)

start_operator = DummyOperator(
    task_id='begin_dag',
    dag=dag
)

get_daily_rates = AlphavantageToPgOperator(
    task_id='get_daily_rates',
    dag=dag
)

# TODO add task to transform reporting tables
# TODO write SQL script to generate table definitions and create tables
# transform_rates = PostgresOperator(
#     task_id='transform_rates',
#     dag=dag
# )

run_jupypter_notebook = PapermillOperator(
    task_id='run_jupyter_notebook',
    input_nb='/usr/local/airflow/notebooks/rates_analysis.ipynb',
    output_nb='/usr/local/airflow/notebooks/rates_analysis.ipynb',
    parameters='',
    start_date=dates.days_ago(1),
    # TODO - test different start_date settings
)

end_operator = DummyOperator(
    task_id='stop_dag',
    dag=dag
)

start_operator >> get_daily_rates
get_daily_rates >> run_jupypter_notebook
run_jupypter_notebook >> end_operator