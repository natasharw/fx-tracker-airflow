
from airflow.plugins_manager import AirflowPlugin
from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook
from alphavantage_plugin.hooks.vonage_api_hook import VonageApiHook
from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator
from alphavantage_plugin.operators.vonage_sms_operator import VonageSmsOperator
from alphavantage_plugin.operators.vonage_tts_operator import VonageTtsOperator

class AlphavantagePlugin(AirflowPlugin):

    name = 'alphavantage_plugin'

    hooks = [AlphavantageHook, VonageApiHook]
    operators = [AlphavantageToS3Operator, VonageSmsOperator, VonageTtsOperator]
    # macros = [my_util_func]
