import os

from airflow.hooks.http_hook import HttpHook

class AlphavantageHook(HttpHook):
    """
    Handles authentication and query request to Alphavantage API

    :param conn_id: name of airflow connection for Alphavantage API
    :type conn_id: str
    :param alphavantage_api_key: access key provided by Alphavantage
    :type alphavantage_api_key: str
    """

    def __init__(
        self,
        conn_id: str,
        *args, **kwargs):

        self.conn_id = conn_id
        self.alphavantage_token = None
        self.alphavantage_token = os.environ.get('ALPHAVANTAGE_API_KEY')
        
        super().__init__(method='GET', http_conn_id=self.conn_id)
    
    def run(self, function: str, from_currency: str, to_currency: str):

        payload = {
            'function': function,
            'from_symbol': from_currency,
            'to_symbol': to_currency,
            'apikey': self.alphavantage_token,
        }

        if self.alphavantage_token:
            return super().run(endpoint='', data=payload)

        # TODO: error handling for when alphavantage token not found
