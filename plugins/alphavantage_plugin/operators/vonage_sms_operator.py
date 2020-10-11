import json
from typing import List
import logging

from airflow.models import BaseOperator

from alphavantage_plugin.hooks.vonage_sms_hook import VonageSmsHook

class VonageSmsOperator(BaseOperator):
    """
    Sends an SMS using Vonage SMS service

    :param vonage_api_conn_id: airflow connection for Vonage APIs
    :type vonage_api_conn_id: str
    :param recipients: list of phone numnbers to send alert to. formatted with the country code and without spaces or plus signs or leading zeros
    :param recipients: str
    """

    def __init__(
        self,
        vonage_api_conn_id: str,
        recipients: List[str],
        message: str,
        *args, **kwargs):

        self.vonage_api_conn_id = vonage_api_conn_id
        self.recipients = recipients
        self.message = message

        super().__init__(*args,**kwargs)


    def _build_payload(self, recipient):
        payload = {
            "from": "VonageAPIBI",
            "to": recipient,
            "text": self.message,
        }
        
        logging.info(f'Payload: {payload}')

        return payload


    def execute(self):
        hook = VonageSmsHook(vonage_api_conn_id=self.vonage_api_conn_id)
        results = []

        for counter, recipient in enumerate(self.recipients,1):
            logging.info(f'Sending SMS to {counter} of {len(self.recipients)} recipients')
            
            payload = self._build_payload(recipient)    

            response = hook.send(payload)
            logging.info(f'Response: {response}')

            msg_cnt = response["message-count"]
            logging.info(f'SMS alert length: {msg_cnt} message(s)')

            for msg in response["messages"]:
                if msg["status"] != "0":
                    msg = f'Vonage SMS send failed. Reason: {msg["error-text"]}'
                    logging.error(msg)

            results += response

        return results


        
