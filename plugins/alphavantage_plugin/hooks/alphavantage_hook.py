from airflow.hooks.http_hook import HttpHook

class AlphavantageHook(HttpHook):

    def __init__(self, alphavantage_conn_id, from_currency, to_currency):
        self.alphavantage_token = None
        self.from_currency = from_currency
        self.to_currency = to_currency
        conn_id = self.get_connection(alphavantage_conn_id)
        if conn_id.extra_dejson.get('token'):
            self.alphavantage_token = conn_id.extra_dejson.get('token')
        super().__init__(method='GET', http_conn_id=alphavantage_conn_id)
    
    def get_conn(self, headers):
        if self.alphavantage_token:
            headers = {'function': 'CURRENCY_EXCHANGE_RATES','apikey': 'token {0}'. format(self.alphavantage_token),'from_currency': '{from_currency}', 'to_currency': '{to_currency}'}
            session = super().get_conn(headers)
            session.auth = None
            return session
        return super().get_conn(headers)
