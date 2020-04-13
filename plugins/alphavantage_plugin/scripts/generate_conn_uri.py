"""
generates a URI to represent an Airflow connection
reference:
https://airflow.apache.org/docs/stable/howto/connection/index.html
format of URI:
my-conn-type://my-login:my-password@my-host:5432/my-schema?param1=val1&param2=val2
"""

import json
from pprint import pprint

from airflow.models.connection import Connection

c = Connection(
    conn_id='alphavantage',
    conn_type='http',
    host='https://www.alphavantage.co/query',
    extra=json.dumps(dict(apikey='YOUR_API_KEY_HERE')),
    )

# print(f"AIRFLOW_CONN_{c.conn_id.upper()}='{c.get_uri()}'")
# [TODO] - investigate 'Connection' object has no attribute 'get_uri'