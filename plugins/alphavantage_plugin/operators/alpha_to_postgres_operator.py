import logging
import json

from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from ..hooks.alphavantage_hook import AlphavantageHook
from airflow.hooks import PostgresHook

class AlphaToPostgresOperator(BaseOperator):
    def __init__(self, to_currency, from_currency, alphavantage_conn_id, postgres_conn_id, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.to_currency = to_currency
        self.from_currency = from_currency
        self.alphavantage_conn_id = alphavantage_conn_id
        self.postgres_conn_id = postgres_conn_id

    def execute(self, context):
        alpha = AlphavantageHook(self.alphavantage_conn_id, self.to_currency, self.from_currency)
        postgres = PostgresHook(self.postgres_conn_id)

        # load data from alpha into postgres