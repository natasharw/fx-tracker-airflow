import logging
import json

from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from airflow.hooks.S3_hook import S3Hook

from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook

logging.basicConfig(level=logging.DEBUG)

class AlphavantageToS3Operator(BaseOperator):
    """
    Fetches a dataset from Alphavantage API and loads into Postgres

    :param conn_id: airflow connection for Alphavantage API
    :type conn_id: str
    :param alphavantage_function: Alphavantage named function to specify which dataset to return
    :type alphavantage_function: str
    :param s3_conn_id: airflow connection for S3
    :type s3_conn_id: str
    :param s3_bucket: target S3 bucket
    :type s3_bucket: str
    :param s3_key: access key for target S3 bucket
    :type s3_key: str
    :const CURRENCY_PAIRS: pairs of three-letter forex currency symbols
    :type CURRENCY_PAIRS: list
    """

    CURRENCY_PAIRS = [
        ('GBP','EUR')
    ]

    def __init__(
        self,
        alphavantage_conn_id: str,
        alphavantage_function: str,
        s3_bucket: str,
        s3_conn_id: str,
        s3_key: str,
        *args, **kwargs):

        self.alphavantage_conn_id = alphavantage_conn_id
        self.alphavantage_function = alphavantage_function
        self.s3_bucket = s3_bucket
        self.s3_conn_id = s3_conn_id
        self.s3_key = s3_key

        super().__init__(*args,**kwargs)

    def execute(self, context):
        data = self.get_data()
        print(data)
        self.load_to_s3(data)

    def get_data(self):
        logging.info("Setting up hook to Alphavantage using conn_id {}".format(self.alphavantage_conn_id))
        alphavantage_hook = AlphavantageHook(conn_id=self.alphavantage_conn_id)
        
        output = []
        for counter, pair in enumerate(self.CURRENCY_PAIRS):
            logging.info("Retrieving data for pair {} of {}".format(counter, len(self.CURRENCY_PAIRS)))
            logging.info("Function: {}, to_currency: {}, from_currency: {}".format(self.alphavantage_function, pair[0], pair[1]))
            response = alphavantage_hook.run(
                function = self.alphavantage_function,
                to_currency = pair[0],
                from_currency = pair[1]
                ).text

            # TODO: format json response
            output = response
            return output

    def load_to_s3(self, data):
        logging.info("Setting up hook to S3 using conn_id {}".format(self.s3_conn_id))
        s3 = S3Hook(self.s3_conn_id)

        logging.info("Loading data into {} bucket".format(self.s3_bucket))
        s3.load_string(
            string_data=data,
            key=self.s3_key,
            bucket_name=self.s3_bucket
        )

        s3.connection.close()
      