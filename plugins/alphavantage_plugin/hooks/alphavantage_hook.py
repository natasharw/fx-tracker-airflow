from airflow.hooks.http_hook import HttpHook

class AlphavantageHook(HttpHook):
    def __init__(self, from_currency: str, to_currency: str, *args, **kwargs):
        self.alphavantage_key = None
        self.conn_id = self.get_connection('alphavantage')
        if self.conn_id.extra_dejson.get('apikey'):
            self.alphavantage_key = self.conn_id.extra_dejson.get('apikey')

        self.from_currency = from_currency
        self.to_currency = to_currency
        
        super().__init__(method='GET', http_conn_id=self.conn_id)
    
    def get_conn(self):
        """
        handles authentication and request to Alphavantage query endpoint
        """

        if self.alphavantage_token:
            headers = {'function': self.QUERY_FUNCTION,'apikey': 'token {0}'. format(self.alphavantage_token),'from_currency': '{from_currency}', 'to_currency': '{to_currency}'}
            session = super().get_conn(headers)
            session.auth = None
            return session
        return super().get_conn(headers)
