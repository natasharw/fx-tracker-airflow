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
from airflow.operators.s3_to_redshift_operator import S3ToRedshiftTransfer
from airflow.utils import dates

from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator


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
s3_conn_id='my_s3_conn_id'
s3_bucket=os.environ.get('S3_BUCKET')
s3_key='daily-exchange-rates-{}'.format(datetime.today().strftime('%Y-%m-%d'))

dag = DAG(
    dag_id='daily_exchange_rates',
    default_args=default_args,
    description='Extract, load, and transform exchange rate data from Alpha Vantage API to Jupyter via S3 and Postgres',
    schedule_interval='0 12 * * *'
)

start_operator = DummyOperator(
    task_id='begin_dag',
    dag=dag
)

# use custom plugin to fetch data from Alpha Vantage API and load to S3
alphavantage_to_s3 = AlphavantageToS3Operator(
    task_id='alphavantage_to_s3',
    alphavantage_function='FX_DAILY',
    alphavantage_conn_id=alphavantage_conn_id,
    s3_conn_id=s3_conn_id,
    s3_bucket=s3_bucket,
    s3_key=s3_key,
    dag=dag
)

# create empty staging table to load data into
create_postgres_staging = PostgresOperator(
    task_id='create_postgres_staging',
    sql='sql/staging/daily_exchange_rates.table.sql',
    dag=dag
)

# populate staging table with new data
s3_to_postgres_staging = S3ToRedshiftTransfer(
    task_id='s3_to_postgres_staging',
    schema='alphavantage',
    table='daily_exchange_rates_staging',
    s3_bucket=s3_bucket,
    s3_key=s3_key,
    redshift_conn_id='postgres_default',
    aws_conn_id='s3_conn_id',
    dag=dag
)

# load only incremental data from staging into main table
load_to_postgres = PostgresOperator(
    task_id='load_to_postgres',
    sql='sql/daily_exchange_rates.sql',
    dag=dag
)

# drop staging table
drop_postgres_staging = PostgresOperator(
    task_id='drop_postgres_staging',
    sql='sql/staging/daily_exchange_rates.drop.sql',
    dag=dag
)

refresh_jupypter_notebook = PapermillOperator(
    task_id='refresh_jupyter_notebook',
    input_nb='/usr/local/airflow/notebooks/rates_analysis.ipynb',
    output_nb='/usr/local/airflow/notebooks/rates_analysis.ipynb',
    parameters='',
    dag=dag
    # TODO - test different start_date settings
)

end_operator = DummyOperator(
    task_id='stop_dag',
    dag=dag
)

start_operator >> alphavantage_to_s3
start_operator >> create_postgres_staging

alphavantage_to_s3 >> s3_to_postgres_staging
create_postgres_staging >> s3_to_postgres_staging

s3_to_postgres_staging >> load_to_postgres

load_to_postgres >> drop_postgres_staging
load_to_postgres >> refresh_jupypter_notebook

drop_postgres_staging >> end_operator
refresh_jupypter_notebook >> end_operator
