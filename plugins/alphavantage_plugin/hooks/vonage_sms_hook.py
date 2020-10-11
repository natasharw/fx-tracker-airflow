import os

from airflow.hooks.base_hook import BaseHook

from vonage import Sms, Client

class VonageSmsHook(BaseHook):
    """
    Handles authentication and query request to Alphavantage API

    :param vonage_api_conn_id: name of airflow connection for Vonage APIs
    :type vonage_api_conn_id: str
    :param alphavantage_api_key: access key provided by Alphavantage
    :type alphavantage_api_key: str
    """

    def __init__(
        self,
        vonage_api_conn_id: str,
        *args, **kwargs):

        self.vonage_api_conn_id = vonage_api_conn_id
    
    def get_conn(self):

        client = Client(key='your_key', secret='your_secret')
        sms = Sms(client)

        return sms

    def send(self, payload):

        sms = self.get_conn()

        return sms.send_message(payload)
