from datetime import datetime
from unittest import TestCase

from airflow.models import DAG, TaskInstance

from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator

class TestAlphaVantageTos3Operator(TestCase):
    def test_execute(self):
        dag = DAG(dag_id='daily_exchange_rates', start_date=datetime.now())
        task = AlphavantageToS3Operator(dag=dag, task_id='alphavantage_to_s3')
        ti = TaskInstance(task=task, execution_date=datetime.now())
        task.execute(ti.get_template_context())
