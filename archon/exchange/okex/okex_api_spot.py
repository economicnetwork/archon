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

class OkexSpot:

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
        server_time = requests.get(base_url + 'api/general/v3/time')
        timestamp = json.loads(server_time.text)['iso']
        request_path = request_path + self.__parse_params_to_str(params)
        url = base_url + request_path
        header = self.__header(self.__signature(timestamp, 'POST', request_path, json.dumps(params)), timestamp)
        body = json.dumps(params)
        response = requests.post(url, data=body, headers=header)
        return response.json()

    def currencies(self):
        return self.__get('/api/account/v3/currencies')

    def wallet(self, currency = ''):
        return self.__get('/api/account/v3/wallet/' + str(currency))

    def transfer(self, currency, amount, type_from, type_to, sub_account = '', instrument_id = ''):

        # type_from: Transaction type for the remitting account (TransactionType.WALLET / SUB, SPOT, FUTURES, C2C, MARGIN, WALLET, ETT)
        # type_to: Transaction type for the beneficiary account (TransactionType.WALLET / SUB, SPOT, FUTURES, C2C, MARGIN, WALLET, ETT)
        #
        # Must fill in sub_account if type_from or type_to = SUB
        #
        # Must fill in instrument_id if type_from or type_to = MARGIN
        #
        # OK06ETT can only be transferred between ETT and SPOT accounts

        params = {'currency': currency, 'amount': amount, 'from': type_from.value, 'to': type_to.value,
                  'sub_account': sub_account, 'instrument_id': instrument_id}
        return self.__post('/api/account/v3/transfer', params)

    def withdrawal(self, currency, amount, exchange_type, address, fee):

        # exchange_type: Destination exchange type (ExchangeType.EXTERN / OKCOIN, OKEX, EXTERN)
        # fee: Network transaction fee≥0. Withdrawals to OKCoin or OKEx are fee-free, so set fee as 0

        params = {'currency': str(currency), 'amount': amount, 'destination': exchange_type.value, 'to_address': str(address),
                  'trade_pwd': self.__fund_password, 'fee': fee}
        return self.__post('/api/account/v3/withdrawal', params)

    def withdrawal_fee(self, currency = ''):
        if currency == '':
            return self.__get('/api/account/v3/withdrawal/fee')
        return self.__get('/api/account/v3/withdrawal/fee', {'currency': currency})

    def withdrawal_history(self, currency = ''):
        return self.__get('/api/account/v3/withdrawal/history/' + currency)

    def ledger(self):
        return self.__get('/api/account/v3/ledger')

    def deposit_address(self, currency):
        return self.__get('/api/account/v3/deposit/address', {'currency': currency})

    def deposit_history(self, currency = ''):
        return self.__get('/api/account/v3/deposit/history/' + str(currency))

    def spot_account(self, currency = ''):
        return self.__get('/api/spot/v3/accounts/' + str(currency))

    def spot_ledger(self, currency, page_from = '', page_to = '', limit = ''):
        params = {}
        if page_from != '':
            params.update({'from': str(page_from)})
        if page_to != '':
            params.update({'to': str(page_to)})
        if page_from != '':
            params.update({'limit': str(limit)})
        if params != {}:
            return self.__get('/api/spot/v3/accounts/' + str(currency) + '/ledger', params)
        return self.__get('/api/spot/v3/accounts/' + str(currency) + '/ledger')

    def place_limit_buy_order(self, symbol, price, size, client_oid = ''):

        # client_oid: order ID customized by yourself
        # symbol: You can use any delimiter 'BTC/USDT' or 'BTC_USDT' or 'BTC-USDT'. Upper case or lower case

        params = {'type': 'limit', 'side': 'buy', 'size': str(size), 'price': str(price),
                  'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if client_oid != '':
            params.update({'client_oid': client_oid})
        return self.__post('/api/spot/v3/orders', params)

    def place_limit_sell_order(self, symbol, price, size, client_oid = ''):

        # client_oid: order ID customized by yourself
        # symbol: You can use any delimiter 'BTC/USDT' or 'BTC_USDT' or 'BTC-USDT'. Upper case or lower case

        params = {'type': 'limit', 'side': 'sell', 'size': str(size), 'price': str(price),
                  'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if client_oid != '':
            params.update({'client_oid': client_oid})
        return self.__post('/api/spot/v3/orders', params)

    def place_market_buy_order(self, symbol, size, client_oid = ''):

        # client_oid: order ID customized by yourself
        # symbol: You can use any delimiter 'BTC/USDT' or 'BTC_USDT' or 'BTC-USDT'. Upper case or lower case

        params = {'type': 'market', 'side': 'buy', 'notional': str(size),
                  'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if client_oid != '':
            params.update({'client_oid': client_oid})
        return self.__post('/api/spot/v3/orders', params)

    def place_market_sell_order(self, symbol, size, client_oid = ''):

        # client_oid: order ID customized by yourself
        # symbol: You can use any delimiter 'BTC/USDT' or 'BTC_USDT' or 'BTC-USDT'. Upper case or lower case

        params = {'type': 'market', 'side': 'sell', 'size': str(size),
                  'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if client_oid != '':
            params.update({'client_oid': client_oid})
        return self.__post('/api/spot/v3/orders', params)

    def cancel_order(self, order_id, symbol):
        params = {"instrument_id": str(symbol.replace('/', '-').replace('_', '-'))}
        return self.__post('/api/spot/v3/cancel_orders/' + str(order_id), params)

    def get_order_list(self, status, symbol, page_from = '', page_to = '', limit = ''):

        # status: status of orders (all, open, part_filled, filled)
        # limit: number of results per request. Maximum 100. (default 100)

        params = {'status': status, 'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if page_from != '':
            params.update({'from': str(page_from)})
        if page_to != '':
            params.update({'to': str(page_to)})
        if limit != '':
            params.update({'limit': str(limit)})
        return self.__get('/api/spot/v3/orders', params)

    def get_all_open_orders(self, symbol = '', page_from = '', page_to = '', limit = ''):
        params = {}
        if symbol != '':
            params.update({'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))})
        if page_from != '':
            params.update({'from': str(page_from)})
        if page_to != '':
            params.update({'to': str(page_to)})
        if limit != '':
            params.update({'limit': str(limit)})
        return self.__get('/api/spot/v3/orders_pending', params)

    def get_order_details(self, order_id, symbol):
        params = {"instrument_id": str(symbol.replace('/', '-').replace('_', '-'))}
        return self.__get('/api/spot/v3/orders/' + str(order_id), params)

    def get_transaction_details(self, order_id, symbol, page_from = '', page_to = '', limit = ''):

        params = {'order_id': order_id, 'instrument_id': str(symbol.replace('/', '-').replace('_', '-'))}
        if page_from != '':
            params.update({'from': str(page_from)})
        if page_to != '':
            params.update({'to': str(page_to)})
        if limit != '':
            params.update({'limit': str(limit)})
        return self.__get('/api/spot/v3/fills', params)

    def get_markets_details(self):
        return self.__get('/api/spot/v3/instruments')

    def get_orderbook(self, symbol, size = '', depth = ''):

        # size: number of results per request. Maximum 200
        # depth: the aggregation of the book. The value is defaulted as the tick_size

        params = {}
        if size != '':
            params.update({'size': str(size)})
        if depth != '':
            params.update({'depth': str(depth)})
        return self.__get('/api/spot/v3/instruments/' + str(symbol.replace('/', '-').replace('_', '-')) + '/book', params)

    def get_ticker(self, symbol = ''):
        if symbol != '':
            return self.__get('/api/spot/v3/instruments/' + str(symbol.replace('/', '-').replace('_', '-')) + '/ticker')
        return self.__get('/api/spot/v3/instruments/ticker')

    def get_trades_details(self, symbol, limit = ''):
        params = {}
        if limit != '':
            params.update({'limit': str(limit)})
        return self.__get('/api/spot/v3/instruments/' + str(symbol.replace('/', '-').replace('_', '-')) + '/trades', params)

    def get_candles(self, symbol, timeframe, start_time = None, end_time = None):

        # The maximum number of data points for a single request is 200 candles.
        # timeframe: TimeFrame.M1 / M1, M3, M5, M15, M30, H1, H2, H4, H12, D1, W1

        params = {'granularity': int(timeframe.value)}
        if start_time is not None:
            params.update({'start': self.__toISO8601(start_time)})
        if end_time is not None:
            params.update({'start': self.__toISO8601(end_time)})
        return self.__get('/api/spot/v3/instruments/' + str(symbol.replace('/', '-').replace('_', '-')) + '/candles', params)