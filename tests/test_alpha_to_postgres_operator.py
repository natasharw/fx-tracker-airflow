from datetime import datetime
from unittest import TestCase

from airflow.models import DAG, TaskInstance

from plugins.alphavantage_plugin.operators.alpha_to_postgres_operator import AlphaToPostgresOperator

class TestAlphaToPostgresOperator(TestCase):
    def test_execute(self):
        dag = DAG(dag_id = 'fx-tracker', start_date=datetime.now*())
        task = AlphaToPostgresOperator(
            dag=dag,
            task_id='load_rates_task',
            to_currency='BTC',
            from_currency='USD',
            alphavantage_conn_id='foo',
            postgres_conn_id='bar'
        )
        ti = TaskInstance(task=task, execution_date=datetime.now())
        task.execute(ti.get_template_context)