from datetime import datetime
from unittest import TestCase

from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator 

class TestAlphavantageToS3Operator(TestCase):
    def setUp(self):
        self.alphavantage_conn_id='alphavantage'
        self.s3_conn_id='my_s3_conn_id'

    def test_check_supported_1(self):
        self.alphavantage_dataset = 'FX_DAILY'
        try:
             AlphavantageToS3Operator.check_supported(self)
        except ValueError:
            self.fail("check_supported() raised ExceptionType unexpectedly!")

    def test_check_supported_2(self):
        self.alphavantage_dataset = 'FOO'
        with self.assertRaises(ValueError):
            AlphavantageToS3Operator.check_supported(self)

    def parse_response_2(self):
        self.alphavantage_dataset = 'FOO'
        with self.assertRaises(ValueError):
            AlphavantageToS3Operator.parse_response(self, '{1,2,3}')
