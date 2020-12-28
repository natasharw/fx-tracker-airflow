import unittest
from unittest.mock import patch, MagicMock

from vonage_plugin.operators.vonage_sms_operator import VonageSmsOperator

class TestVonageSmsOperator(unittest.TestCase):

    def setUp(self):
        self.vonage_api_conn_id = 'test_conn_id'
        self.recipients = ['111111', '22222', '3333', '444']
        self.message = 'I am a test'
        self.mock_resposnse_json = {'foo': 'bar'}

    @patch('alphavantage_plugin.operators.vonage_sms_operator.VonageApiHook')
    def test__build_payload(self, mock_hook):

        test_operator = VonageSmsOperator(
            task_id='this_is_a_test',
            vonage_api_conn_id=self.vonage_api_conn_id,
            recipients=self.recipients,
            message=self.message)

        expected_result =  {
            "from": "VonageAPIBI",
            "to": '111111',
            "text": 'I am a test',
        }

        actual_result = test_operator._build_payload(self.recipients[0])

        self.assertEqual(actual_result, expected_result)

    @patch.object(VonageSmsOperator, '_handle_response')
    @patch.object(VonageSmsOperator, '_build_payload')
    @patch('alphavantage_plugin.operators.vonage_sms_operator.VonageApiHook')
    def test_execute(self, mock_hook, mock_build_payload, mock_handle_response):
        test_operator = VonageSmsOperator(
            task_id='this_is_a_test',
            vonage_api_conn_id=self.vonage_api_conn_id,
            recipients=self.recipients,
            message=self.message)

        # mock_hook.send_sms.return_value = 'blah'

        expected_call_count = len(self.recipients)
        mock_handle_response.return_value = self.mock_resposnse_json

        actual_result = test_operator.execute()

        self.assertEqual(mock_handle_response.call_count, expected_call_count)
        self.assertEqual(mock_build_payload.call_count, expected_call_count)

        self.assertEqual(actual_result, [
            {'foo': 'bar'},
            {'foo': 'bar'},
            {'foo': 'bar'},
            {'foo': 'bar'}])


    # @patch('plugins.alphavantage_plugin.operators.vonage_sms_operator.VonageApiHook')
    # def test__handle_response(self, mock_hook):
    #     test_operator = VonageSmsOperator(
    #         task_id='this_is_a_test',
    #         vonage_api_conn_id=self.vonage_api_conn_id,
    #         recipients=self.recipients,
    #         message=self.message)

    #     mock_response = MagicMock()
    #     mock_response["messages"] = [
    #             {"status": 1,
    #             "error-text": "some_error"}]
    #     mock_response.json.return_value = {
    #         "message-count": 1,
    #         "messages": [
    #             {"status": 1,
    #             "error-text": "some_error"}]}
        
    #     print("DEBUGDEBUG" + mock_response["messages"])
        
    #     with self.assertRaises(ValueError):
    #         test_operator._handle_response(mock_response)
