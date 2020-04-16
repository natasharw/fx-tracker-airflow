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

alphavantage_conn_id='alphavantage'


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

# create empty staging table to load data into
create_staging = PostgresOperator(
    task_id='create_staging',
    sql='sql/staging/daily_exchange_rates.table.sql',
    dag=dag
)

# populate staging table with new data
populate_staging = AlphavantageToPgOperator(
    task_id='load_rates_to_staging',
    function='FX_DAILY',
    alphavantage_conn_id=alphavantage_conn_id,
    postgres_table='alphavantage.daily_exchange_rates_staging',
    dag=dag
)

# load only incremental data from staging into main table
load_exchange_rates = PostgresOperator(
    task_id='load_exchange_rates',
    sql='sql/daily_exchange_rates.sql',
    dag=dag
)

# drop staging table
drop_staging = PostgresOperator(
    task_id='drop_staging',
    sql='sql/staging/daily_exchange_rates.drop.sql',
    dag=dag
)

# TODO transform data to reporting tables
# transform_rates = PostgresOperator(
#     task_id='transform_rates',
#     dag=dag
# )

refresh_jupypter_notebook = PapermillOperator(
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

start_operator >> create_staging >> populate_staging
populate_staging >> load_exchange_rates >> drop_staging
drop_staging >> refresh_jupypter_notebook >> end_operator
