
from airflow.plugins_manager import AirflowPlugin
from vonage_plugin.hooks.vonage_api_hook import VonageApiHook
from vonage_plugin.operators.vonage_sms_operator import VonageSmsOperator
from vonage_plugin.operators.vonage_tts_operator import VonageTtsOperator

class VonagePlugin(AirflowPlugin):

    name = 'vonage_plugin'

    hooks = [VonageApiHook]
    operators = [VonageSmsOperator, VonageTtsOperator]
