from datetime import datetime
from unittest import TestCase

from airflow.models import DAG, TaskInstance
from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator 

class TestAlphavantageToS3Operator(TestCase):
    def setUp(self):
        self.alphavantage_conn_id='alphavantage'
        self.s3_conn_id='my_s3_conn_id'

    def test_check_supported_1(self):
        self.alphavantage_dataset = 'FX_DAILY'
        func = AlphavantageToS3Operator.check_supported(self)
        self.assertEqual(func,0)

    def test_check_supported_2(self):
        self.alphavantage_dataset = 'FOO'
        self.assertRaises(ValueError, AlphavantageToS3Operator.check_supported(self))

    def parse_response_2(self):
        self.alphavantage_dataset = 'FOO'
        self.assertRaises(ValueError, AlphavantageToS3Operator.parse_response(self, '{1,2,3}'))


    # def test_execute(self):
    #     dag = DAG(dag_id='daily_exchange_rates',start_date=datetime.now())
    #     task = AlphavantageToS3Operator(
    #         dag=dag,
    #         task_id='s3_to_postgres_pre_staging'
    #         aws_conn_id='s3_conn_id',
    #         s3_bucket=s3_bucket,
    #         s3_key=s3_key,
    #         redshift_conn_id='postgres_default',
    #         schema='alphavantage',
    #         table='daily_exchange_rates_pre_staging',
    #         dag=dag)
    #     ti = TaskInstance(task=task, execution_date=datetime.now())
    #     task.execute(ti.get_template_context())
