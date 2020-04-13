import logging
import json

from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook

class AlphavantageToPgOperator(BaseOperator):
    CURRENCY_PAIRS = [
        ('BTC','USD')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def execute(self, context):
        data = self.get_data()
        self.load_data(data)

    def get_data(self):
        for pair in self.CURRENCY_PAIRS:
            from_currency = pair[0]
            to_currency = pair[1]
            # TODO: for each currency pair, add data to local tmp file
            data = AlphavantageHook(from_currency, to_currency)
            print('returning data')
            return data
    
    def load_data(self, data):
        # TODO: persist local tmp file to postgres
        # postgres = PostgresHook(self.postgres_conn_id)
        print('the custom alphavantage to postgres operator is a work in progress..!')
      