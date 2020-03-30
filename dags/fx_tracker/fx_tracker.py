from datetime import datetime, timedelta
import json
import requests

import redis
from airflow.hooks.http_hook import HttpHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook
from alphavantage_plugin.operators.alpha_to_postgres_operator import AlphaToPostgresOperator

def get_rates(ds, **kwargs):
    load_data()
    # json_data = get_json_data()
    # clean_rates = clean_rates()

    # response = api_hook.run('')
    # response = json.loads(response.content)
    # # valid_pairs
    # # rates_insert

def load_data():
    api_hook = AlphavantageHook(alphavantage_conn_id='alphavantage', from_currency='BTC', to_currency='USD')

    response = api_hook.run('')
    print(response)
    # pg_hook = PostgresHook(postgres_conn_id='airflow')

    # file_name = str(datetime.now().date() + '.json')
    # api_hook = HttpHook(http_conn_id='aplhavantage', method='GET')

    # baseurl = 'https://www.alphavantage.co/query'
    # params = {"function":"DIGITAL_CURRENCY_DAILY","symbol":"BTC", "market":"CNY", "apikey":"PYHXPK6P2IDF77IS"}
            
    # r2= requests.get(baseurl, params=params)

def clean_rates():
    # do nothing for now
    print('skipping as clean rates() is work in progress')


def cache_latest_rates(ds, **kwargs):
    # do nothing for now
    print('skipping as cache_latest_rates() is work in progress')

args = {
    'owner': 'natasha',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(dag_id='fx_tracker',
            default_args=args,
            schedule_interval = '0 * * * 1,2,3,4,5',
            dagrun_timeout=timedelta(seconds=30)
)

load_rates_task = AlphaToPostgresOperator(task_id='get_rates',
                                provide_context=True,
                                python_callable=get_rates,
                                dag=dag)

cache_latest_rates_task = PythonOperator(task_id='cache_latest_rates',
                            provide_context=True,
                            python_callable=cache_latest_rates,
                            dag=dag)

load_rates_task.set_downstream(cache_latest_rates_task)
