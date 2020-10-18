
import json
from typing import List
import logging

from airflow.models import BaseOperator

from alphavantage_plugin.hooks.vonage_api_hook import VonageApiHook

class VonageTtsOperator(BaseOperator):
    """
    Makes an automated call using Vonage Text-To-Speech service

    :param vonage_api_conn_id: airflow connection for Vonage APIs
    :type vonage_api_conn_id: str
    :param recipients: list of phone numnbers to send alert to. formatted with the country code and without spaces or plus signs or leading zeros
    :param recipients: str
    :param message: text body of the SMS to be sent
    :param message: str
    """

    def __init__(
        self,
        vonage_api_conn_id: str,
        # recipients: List[str],
        # message: str,
        *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.vonage_api_conn_id = vonage_api_conn_id
        # self.recipients = recipients
        # self.message = message

    def execute(self):
        hook = VonageApiHook(vonage_api_conn_id=self.vonage_api_conn_id)
        payload = self._build_payload()
        response = hook.make_automated_call(payload)

        print(response)

    def _build_payload(self):
        to_number = [{'type': 'phone', 'number': 'ADD_PHONE_NUMBER'}]
        from_number = [{'type': 'phone', 'number': 'ADD_PHONE_NUMBER'}]
        ncco = [
                {
                "action": "talk",
                "text": "There has been a failure on Airflow"
                }
            ]

        payload = {
            'to': to_number,
            'from': from_number,
            'ncco': ncco
        }

        return payload
