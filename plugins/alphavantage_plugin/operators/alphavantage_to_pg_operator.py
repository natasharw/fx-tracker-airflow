import logging
import json

from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook

class AlphavantageToPgOperator(BaseOperator):
    """
    Fetches a dataset from Alphavantage API and loads into Postgres

    :param conn_id: name of airflow connection for Alphavantage API
    :type conn_id: str
    :param function: Alphavantage named function to specify which dataset to return
    :type function: str
    :param postgres_conn_id: name of airflow connection for postgres instance
    :type postgres_conn_id: str
    :param postgres_table: target postgres table referenced as SCHEMA_NAME.TABLE_NAME
    :type postgres_table: str
    :const CURRENCY_PAIRS: pairs of three-letter forex currency symbols
    :type CURRENCY_PAIRS: list
    """

    CURRENCY_PAIRS = [
        ('GBP','EUR')
    ]

    def __init__(
        self,
        alphavantage_conn_id: str,
        function: str,
        postgres_table: str,
        postgres_conn_id='postgres_default',
        *args, **kwargs):

        self.alphavantage_conn_id = alphavantage_conn_id
        self.function = function
        super().__init__(*args,**kwargs)

    def execute(self, context):
        data = self.get_data()
        print(data)
        self.load_data(data)

    def get_data(self):
        output = []
        for pair in self.CURRENCY_PAIRS:
            response = AlphavantageHook(conn_id=self.alphavantage_conn_id).run(
                function = self.function,
                to_currency = pair[0],
                from_currency = pair[1]).text

            print(response)
            print(output)

            return output

            # TODO: parse the json and add to output


    def load_data(self, data):
        # TODO: persist output to postgres
        # postgres = PostgresHook(self.postgres_conn_id)
        print('the custom alphavantage to postgres operator is a work in progress..!')
      