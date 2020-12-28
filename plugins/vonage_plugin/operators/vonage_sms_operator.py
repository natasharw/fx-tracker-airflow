import json
from typing import List
import logging

from airflow.models import BaseOperator

from vonage_plugin.hooks.vonage_api_hook import VonageApiHook

class VonageSmsOperator(BaseOperator):
    """
    Sends SMS messages using Vonage API SMS service

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
        recipients: List[str],
        message: str,
        *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.vonage_api_conn_id = vonage_api_conn_id
        self.recipients = recipients
        self.message = message

    def execute(self):
        hook = VonageApiHook(vonage_api_conn_id=self.vonage_api_conn_id)
        results = []

        for counter, recipient in enumerate(self.recipients,1):
            logging.info(f'Sending SMS to {counter} of {len(self.recipients)} recipients')
            
            payload = self._build_payload(recipient)    
            response = hook.send_sms(payload)
            result = self._handle_response(response)

            results.append(result)

        return results

    def _build_payload(self, recipient):
        payload = {
            "from": "VonageAPIBI",
            "to": recipient,
            "text": self.message,
        }
        
        logging.info(f'Payload: {payload}')

        return payload

    def _handle_response(self, response):
        logging.info(f'Response from Vonage API: {response}')
        logging.info(f'Messages sent: {response["message-count"]}')

        for message in response["messages"]:
            self._check_message_status(message)

        return response
    
    @staticmethod
    def _check_message_status(message):    
        if message["status"] != "0":
            message = f'Vonage SMS send failed. Reason: {message["error-text"]}'
            raise ValueError(message)
