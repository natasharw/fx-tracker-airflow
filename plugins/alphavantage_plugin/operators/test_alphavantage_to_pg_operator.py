from datetime import datetime
from unittest import TestCase

from airflow.models import DAG, TaskInstance

from alphavantage_plugin.operators.alphavantage_to_pg_operator import AlphavantageToPgOperator

class TestAlphavantageToPgOperator(TestCase):
    def test_execute(self):
        dag = DAG(dag_id='daily_exchange_rates', start_date=datetime.now())
        task = AlphavantageToPgOperator(dag=dag, task_id='get_daily_rates')
        ti = TaskInstance(task=task, execution_date=datetime.now())
        task.execute(ti.get_template_context())