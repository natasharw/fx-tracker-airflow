
from airflow.plugins_manager import AirflowPlugin
from alphavantage_plugin.hooks.alphavantage_hook import AlphavantageHook
from alphavantage_plugin.operators.alphavantage_to_s3_operator import AlphavantageToS3Operator

class AlphavantagePlugin(AirflowPlugin):

    name = 'alphavantage_plugin'

    hooks = [AlphavantageHook]
    operators = [AlphavantageToS3Operator]
    # macros = [my_util_func]
