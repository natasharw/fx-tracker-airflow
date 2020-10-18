import json
import logging

from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from alphavantage_plugin.constants import SUPPORTED
from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook

class AlphavantageToS3Operator(BaseOperator):
    """
    Fetches dataset from Alphavantage API and loads json into S3

    :param alphavantage_conn_id: airflow connection for Alphavantage API
    :type alphavantage_conn_id: str
    :param alphavantage_dataset: Alphavantage named dataset to return
    :type alphavantage_dataset: str
    :param s3_conn_id: airflow connection for S3
    :type s3_conn_id: str
    :param s3_bucket: target S3 bucket
    :type s3_bucket: str
    :param s3_key: target file name in S3 bucket
    :type s3_key: str
    :param currencies: currencies to query data for
    :type: list
    """

    def __init__(
        self,
        alphavantage_conn_id: str,
        alphavantage_dataset: str,
        s3_bucket: str,
        s3_conn_id: str,
        s3_key: str,
        currencies: list,
        *args, **kwargs):

        self.alphavantage_conn_id = alphavantage_conn_id
        self.alphavantage_dataset = alphavantage_dataset
        self.s3_conn_id = s3_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.currencies = currencies

        super().__init__(*args,**kwargs)

    def execute(self, context):
        data = self.get_data()
        self.load_to_s3(data)

    def get_data(self):
        logging.info("Setting up hook to Alphavantage using conn_id {}".format(self.alphavantage_conn_id))
        alphavantage_hook = AlphavantageHook(conn_id=self.alphavantage_conn_id)

        self.check_supported()
        
        output = []
        for counter, pair in enumerate(self.currencies):
            logging.info("Retrieving data for pair {} of {}".format(counter+1, len(self.currencies)))
            logging.info("Function: {}, to_currency: {}, from_currency: {}".format(self.alphavantage_dataset, pair[0], pair[1]))

            response = self.request_data(alphavantage_hook, pair)
            formatted = self.parse_response(response)
            output = '\n'.join(formatted)
            return output

    def request_data(self, alphavantage_hook: str, pair: tuple):
        logging.info("Requesting data from Alpha Vantage API")
        try:
            response = alphavantage_hook.run(
                function = self.alphavantage_dataset,
                to_currency = pair[0],
                from_currency = pair[1]
                ).text

            logging.info("Request successful")
            logging.info("Response: {}".format(response))
            return response
        except:
            logging.info("Could not return {} for currency pair {},{}".format(self.alphavantage_dataset, pair[0], pair[1]))
            return response

    def check_supported(self):
        logging.info("Checking {} dataset is supported".format(self.alphavantage_dataset))
        if self.alphavantage_dataset not in SUPPORTED:
            raise ValueError("{} not in supported datasets".format(self.alphavantage_dataset))
        logging.info("Check successful")
        return 0

    def parse_response(self, response: str):
        logging.info("Parsing json")
        if self.alphavantage_dataset == 'FX_DAILY':
            formatted = self.parse_fx_daily(response)
            return formatted
        else:
            raise ValueError("The only supported datasets right now are {}".format(SUPPORTED))

    def parse_fx_daily(self, response: str):
        logging.info("Using parsing rules for FX Daily")

        json = eval(response)
        formatted = []

        for k, v in json['Time Series FX (Daily)'].items():
            v['date'] = k
            v['from_symbol'] = json['Meta Data']['2. From Symbol']
            v['to_symbol'] = json['Meta Data']['3. To Symbol']
            formatted.append(v)

        return formatted

    def load_to_s3(self, data: str):
        logging.info("Setting up hook to S3 using conn_id {}".format(self.s3_conn_id))
        s3 = S3Hook(self.s3_conn_id)

        logging.info("Loading json into {} bucket".format(self.s3_bucket))
        s3.load_string(
            string_data=data,
            key=self.s3_key+'_json',
            bucket_name=self.s3_bucket
        )
      