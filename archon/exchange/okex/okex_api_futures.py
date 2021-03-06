import json
import hmac
import base64
import requests
import datetime
import urllib.parse
from enum import Enum

class TransactionType(Enum):
    SUB = 0
    SPOT = 1
    FUTURES = 3
    C2C = 4
    MARGIN = 5
    WALLET = 6
    ETT = 7

class ExchangeType(Enum):
    OKCOIN = 2
    OKEX = 3
    EXTERN = 4

class TimeFrame(Enum):
    M1 = 60
    M3 = 180
    M5 = 300
    M15 = 900
    M30 = 1800
    H1 = 3600
    H2 = 7200
    H4 = 14400
    H12 = 43200
    D1 = 86400
    W1 = 604800

base_url = 'https://www.okex.com'

class OkexFutures:

    def __init__(self, api_key, secret_key, passphrase, fund_password):
        """Constructor"""
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__passphrase = passphrase
        self.__fund_password = fund_password

    def __toISO8601(self, time):
        return time.replace(tzinfo=datetime.timezone.utc).isoformat().split('+')[0] + 'Z'

    # signature
    def __signature(self, timestamp, method, request_path, body):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(self.__secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    # set request header
    def __header(self, sign, timestamp):
        header = dict()
        header['Content-Type'] = 'application/json'
        header['OK-ACCESS-KEY'] = self.__api_key
        header['OK-ACCESS-SIGN'] = sign
        header['OK-ACCESS-TIMESTAMP'] = str(timestamp)
        header['OK-ACCESS-PASSPHRASE'] = self.__passphrase
        return header

    def __parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + urllib.parse.quote(str(value), safe='') + '&'
        return url[0:-1]

    def __get(self, request_path, params = {}):
        
        server_time = requests.get(base_url + '/api/general/v3/time')
        timestamp = json.loads(server_time.text)['iso']
        request_path = request_path + self.__parse_params_to_str(params)
        header = self.__header(self.__signature(timestamp, 'GET', request_path, None), timestamp)
        response = requests.get(base_url + request_path, headers=header)
        return response.json()

    def __post(self, request_path, params):
        server_time = requests.get(base_url + '/api/general/v3/time')
        timestamp = json.loads(server_time.text)['iso']
        request_path = request_path + self.__parse_params_to_str(params)
        url = base_url + request_path
        header = self.__header(self.__signature(timestamp, 'POST', request_path, json.dumps(params)), timestamp)
        body = json.dumps(params)
        response = requests.post(url, data=body, headers=header)
        return response.json()

    def get_position(self):
        return self.__get('/api/futures/v3/position')

    def order_list(self, instrument_id):    
        state = '0' #Order Status: -2 = Failed -1 = Canceled 0 = Open 1 = Partially Filled 2 = Fully Filled 3 = Submitting 4 = Canceling 6 = Incomplete (open + partially filled) 7 = Complete (canceled + fully filled)
        path = "/api/futures/v3/orders/" + instrument_id
        params = {'state': state}
        return self.__get(path, params)


    def submit_example(self, instrument_id, price):
        """
        #instrument_id	String Yes Contract ID,e.g. BTC-USD-180213 ,BTC-USDT-191227
        type	String	Yes	1:open long 2:open short 3:close long 4:close short
        price	String	Yes	Price of each contract
        size	String	Yes	The buying or selling quantity
        """        
        otype = '1'
        size = '10'
        params = {'instrument_id': instrument_id, 'type': otype, 'price': price, 'size': size}
        result = self.__post('/api/futures/v3/order', params)
        print ("result ", result)

    def orderbook(self, instrument_id):
        #GET /api/futures/v3/instruments/<instrument_id>/book
        params = {'instrument_id': instrument_id}
        path = "/api/futures/v3/instruments/" + instrument_id + "/book"
        params = {'size': 2}
        result = self.__get(path, params)
        return result

