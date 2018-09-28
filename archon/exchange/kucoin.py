# coding=utf-8
#https://kucoinapidocs.docs.apiary.io/
import base64
import hashlib
import hmac
import time
import requests
import json

#from .exceptions import KucoinAPIException, KucoinRequestException, KucoinResolutionException
#from .helpers import date_to_seconds

import dateparser
import pytz

from datetime import datetime


def date_to_seconds(date_str):
    """Convert UTC date to seconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds())
    
class KucoinAPIException(Exception):
    """Exception class to handle general API Exceptions
        `code` values
        `message` format
    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.message = json_res['error']
            if 'msg' in json_res:
                self.message = json_res['msg']
            if 'message' in json_res and json_res['message'] != 'No message available':
                self.message += ' - {}'.format(json_res['message'])
            if 'code' in json_res:
                self.code = json_res['code']
            if 'data' in json_res:
                try:
                    self.message += " " + json.dumps(json_res['data'])
                except ValueError:
                    pass

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'KucoinAPIException {}: {}'.format(self.code, self.message)


class KucoinRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'KucoinRequestException: {}'.format(self.message)


class KucoinResolutionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'KucoinResolutionException: {}'.format(self.message)

class KuClient(object):

    API_URL = 'https://api.kucoin.com'
    API_VERSION = 'v1'
    _language = 'en-US'

    _last_timestamp = None

    TRANSFER_WITHDRAWAL = 'WITHDRAW'
    TRANSFER_DEPOSIT = 'DEPOSIT'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    TRANSFER_STATUS_CANCELLED = 'CANCEL'
    TRANSFER_STATUS_PENDING = 'PENDING'
    TRANSFER_STATUS_FINISHED = 'FINISHED'

    RESOLUTION_1MINUTE = '1'
    RESOLUTION_5MINUTES = '5'
    RESOLUTION_15MINUTES = '15'
    RESOLUTION_30MINUTES = '30'
    RESOLUTION_1HOUR = '60'
    RESOLUTION_8HOURS = '480'
    RESOLUTION_1DAY = 'D'
    RESOLUTION_1WEEK = 'W'

    _resolution_map = {
        RESOLUTION_1MINUTE: '1min',
        RESOLUTION_5MINUTES: '5min',
        RESOLUTION_15MINUTES: '15min',
        RESOLUTION_30MINUTES: '30min',
        RESOLUTION_1HOUR: '1hour',
        RESOLUTION_8HOURS: '8hour',
        RESOLUTION_1DAY: '1day',
        RESOLUTION_1WEEK: '1week',
    }

    def __init__(self, api_key, api_secret, language=None, requests_params=None):
        """Kucoin API Client constructor

        https://kucoinapidocs.docs.apiary.io/

        :param api_key: Api Token Id
        :type api_key: string
        :param api_secret: Api Secret
        :type api_secret: string
        :param requests_params: optional - Dictionary of requests params to use for all calls
        :type requests_params: dict.

        .. code:: python

            client = Client(api_key, api_secret)

        """

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        if language:
            self._language = language
        self._requests_params = requests_params
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-kucoin',
                   'KC-API-KEY': self.API_KEY,
                   'HTTP_ACCEPT_LANGUAGE': self._language,
                   'Accept-Language': self._language}
        session.headers.update(headers)
        return session

    def _order_params_for_sig(self, data):
        """Convert params to ordered string for signature

        :param data:
        :return: ordered parameters like amount=10&price=1.1&type=BUY

        """
        strs = []
        for key in sorted(data):
            strs.append("{}={}".format(key, data[key]))
        return '&'.join(strs)

    def _generate_signature(self, path, data, nonce):
        """Generate the call signature

        :param path:
        :param data:
        :param nonce:

        :return: signature string

        """

        query_string = self._order_params_for_sig(data)
        sig_str = ("{}/{}/{}".format(path, nonce, query_string)).encode('utf-8')
        m = hmac.new(self.API_SECRET.encode('utf-8'), base64.b64encode(sig_str), hashlib.sha256)
        return m.hexdigest()

    def _create_path(self, method, path):
        return '/{}/{}'.format(self.API_VERSION, path)

    def _create_uri(self, path):
        return '{}{}'.format(self.API_URL, path)

    def _request(self, method, path, signed, **kwargs):

        # set default requests timeout
        kwargs['timeout'] = 10

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        kwargs['data'] = kwargs.get('data', {})
        kwargs['headers'] = kwargs.get('headers', {})

        full_path = self._create_path(method, path)
        uri = self._create_uri(full_path)

        if signed:
            # generate signature
            nonce = int(time.time() * 1000)
            kwargs['headers']['KC-API-NONCE'] = str(nonce)
            kwargs['headers']['KC-API-SIGNATURE'] = self._generate_signature(full_path, kwargs['data'], nonce)

        if kwargs['data'] and method == 'get':
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith('2'):
            raise KucoinAPIException(response)
        try:
            json = response.json()

            if 'success' in json and not json['success']:
                raise KucoinAPIException(response)

            self._last_timestamp = None
            if 'timestamp' in json:
                self._last_timestamp = json['timestamp']

            # by default return full response
            res = json
            # if it's a normal response we have a data attribute, return that
            if 'data' in json:
                res = json['data']
            return res
        except ValueError:
            raise KucoinRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    def get_last_timestamp(self):
        """Get the server timestamp for the last request

        :return: response timestamp in ms

        """
        return self._last_timestamp

    # User API Endpoints

    def create_api_key(self):
        """Create a new API Key
        :raises:  KucoinResponseException, KucoinAPIException

        """

        return self._post('api/create', True)

    def update_api_key(self, key, enabled=None, remark=None, permissions=None):
        """Update an API Key
        https://kucoinapidocs.docs.apiary.io/#reference/0/user-api-management/update-api-key
        """

        data = {
            'key': key
        }
        if enabled is not None:
            data['enabled'] = enabled
        if remark:
            data['remark'] = remark
        if permissions:
            data['permissions'] = permissions

        return self._post('api/update', True, data=data)

    def get_api_keys(self):
        """Get list of API Keys
        :returns: API Response
        :raises:  KucoinResponseException, KucoinAPIException

        """

        return self._get('api/list', True)

    def delete_api_key(self, key):
        """Update an API Key
        """

        data = {
            'key': key
        }

        return self._post('api/delete', True, data=data)

    # Currency Endpoints

    def get_currencies(self, coins=None):
        """List the exchange rate of coins
        https://kucoinapidocs.docs.apiary.io/#reference/0/currencies-plugin/list-exchange-rate-of-coins(open)
        """

        data = {}
        if coins:
            if type(coins) != list:
                coins = [coins]
            data['coins'] = ','.join(coins)

        return self._get('open/currencies', False, data=data)

    def set_default_currency(self, currency):
        """Set your default currency"""
        data = {
            'currency': currency
        }

        return self._post('user/change-currency', False, data=data)

    """
    # Language Endpoints

    def get_languages(self):        
        return self._get('open/lang-list')

    # User Endpoints

    def update_language(self, language):        
        data = {
            'lang': language
        }
        return self._post('user/change-lang', True, data=data)
    """

    def get_user(self):
        """Get user info

        https://kucoinapidocs.docs.apiary.io/#reference/0/user/get-user-info

        .. code:: python

            user = client.get_user()

        :returns: ApiResponse
        """

        return self._get('user/info', True)

    # Invitation Endpoints

    def get_invite_count(self):
        """Get invite count
        """

        return self._get('referrer/descendant/count', True)

    def get_reward_info(self, coin=None):
        """Get promotion reward info all coins or an individual coin
        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._get('account/promotion/info', True, data=data)

    def get_reward_summary(self, coin=None):
        """Get promotion reward summary for all coins or a specific coin
        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._get('account/promotion/sum', True, data=data)

    def extract_invite_bonus(self, coin=None):
        """Extract the invitation bonus for all coins or a specific coin
        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._post('account/promotion/draw', True, data=data)

    # Asset Endpoints

    def get_deposit_address(self, coin):
        """Get deposit address for a coin
        """

        return self._get('account/{}/wallet/address'.format(coin), True)

    def create_withdrawal(self, coin, amount, address):
        """Get deposit address for a coin
        """

        data = {
            'amount': amount,
            'address': address
        }

        return self._post('account/{}/withdraw/apply'.format(coin), True, data=data)

    def cancel_withdrawal(self, coin, txid):
        """Cancel a withdrawal
        """

        data = {
            'txOid': txid
        }

        return self._get('account/{}/withdraw/cancel'.format(coin), True, data=data)

    def get_deposits(self, coin, status=None, limit=None, page=None):
        """Get deposit records for a coin
        """

        data = {
            'type': self.TRANSFER_DEPOSIT
        }
        if status:
            data['status'] = status
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/{}/wallet/records'.format(coin), True, data=data)

    def get_withdrawals(self, coin, status=None, limit=None, page=None):
        """Get withdrawal records for a coin
        """

        data = {
            'type': self.TRANSFER_WITHDRAWAL
        }
        if status:
            data['status'] = status
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/{}/wallet/records'.format(coin), True, data=data)

    def get_coin_balance(self, coin):
        """Get balance of a coin"""

        return self._get('account/{}/balance'.format(coin), True)

    def get_all_balances(self):
        """Get all coin balances"""
        data = {}

        return self._get('account/balance', True, data=data)

    def get_all_balances_paged(self, limit=None, page=None):
        """Get all coin balances with paging if that's what you want"""

        data = {}
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/balances', True, data=data)


    # Trading Endpoints

    def create_order(self, symbol, order_type, price, amount):

        data = {
            'symbol': symbol,
            'type': order_type,
            'price': price,
            'amount': amount
        }

        return self._post('order', True, data=data)

    def create_buy_order(self, symbol, price, amount):

        return self.create_order(symbol, self.SIDE_BUY, price, amount)

    def create_sell_order(self, symbol, price, amount):

        return self.create_order(symbol, self.SIDE_SELL, price, amount)

    def get_active_orders(self, symbol, kv_format=False):
        """Get list of active orders"""

        data = {
            'symbol': symbol
        }

        path = 'order/active'
        if kv_format:
            path += '-map'

        return self._get(path, True, data=data)

    def cancel_order(self, order_id, order_type, symbol=None):
        """Cancel an order"""
        print ("cancel " + str(order_id) + " " + str(order_type))
        print (symbol)
        data = {
            'orderOid': order_id
        }

        if order_type:
            data['type'] = order_type
        if symbol:
            data['symbol'] = symbol

        return self._post('cancel-order', True, data=data)

    def cancel_all_orders(self, symbol=None, order_type=None):
        """Cancel all orders"""

        data = {}
        if order_type:
            data['type'] = order_type
        if symbol:
            data['symbol'] = symbol

        return self._post('order/cancel-all', True, data=data)

    def get_dealt_orders(self, symbol=None, order_type=None, limit=None, page=None, since=None, before=None):
        """Get a list of dealt orders with pagination
        """

        data = {}
        if symbol:
            data['symbol'] = symbol
        if order_type:
            data['type'] = order_type
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page
        if since:
            data['since'] = since
        if before:
            data['before'] = before

        return self._get('order/dealt', True, data=data)

    def get_symbol_dealt_orders(self, symbol, order_type=None, limit=None, page=None):
        """Get a list of dealt orders for a specific symbol with pagination

        """

        data = {
            'symbol': symbol
        }
        if order_type:
            data['type'] = order_type
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('deal-orders', True, data=data)

    def get_order_details(self, symbol, order_type, limit=None, page=None, order_id=None):
        """Get order details

        """

        data = {
            'symbol': symbol,
            'type': order_type
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page
        if order_id:
            data['orderOid'] = order_id

        return self._get('order/detail', True, data=data)

    # Market Endpoints

    def get_tick(self, symbol=None):
        """Get all ticks or a symbol tick"""

        data = {}
        if symbol:
            data['symbol'] = symbol

        return self._get('open/tick', False, data=data)

    def get_order_book(self, symbol, group=None, limit=None):
        """Get the order book for a symbol"""

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders', False, data=data)

    def get_buy_orders(self, symbol, group=None, limit=None):
        """Get the buy orders for a symbol

        """

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders-buy', False, data=data)

    def get_sell_orders(self, symbol, group=None, limit=None):
        """Get the sell orders for a symbol

        """

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders-sell', False, data=data)

    def get_recent_orders(self, symbol, limit=None, since=None):
        """Get recent orders"""

        data = {
            'symbol': symbol
        }
        if limit:
            data['limit'] = limit
        if since:
            data['since'] = since

        return self._get('open/deal-orders', False, data=data)

    def get_trading_markets(self):
        """Get list of trading markets

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trading-markets(open)

        .. code:: python

            coins = client.get_trading_markets()

        :returns: ApiResponse

        .. code:: python

            [
                "BTC",
                "ETH",
                "NEO",
                "USDT"
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self._get('open/markets')

    def get_trading_symbols(self, market=None):
        """Get list of trading symbols for an optional market

        """

        data = {}
        if market:
            data['market'] = market

        return self._get('market/open/symbols', False, data=data)

    def get_trending_coins(self, market=None):
        """Get list of trending coins for an optional market

        """
        data = {}
        if market:
            data['market'] = market

        return self._get('market/open/coins-trending', False, data=data)

    def get_kline_data(self, symbol, resolution, from_time, to_time, limit=None):
        """Get kline data

        """

        try:
            resolution = self._resolution_map[resolution]
        except KeyError:
            raise KucoinResolutionException('Invalid resolution passed')

        data = {
            'symbol': symbol,
            'type': resolution,
            'from': from_time,
            'to': to_time
        }
        if limit:
            data['limit'] = limit

        return self._get('open/kline', False, data=data)

    def get_kline_config_tv(self):
        """Get kline config (TradingView version)

        """

        return self._get('open/chart/config')

    def get_symbol_tv(self, symbol):
        """Get symbol data (TradingView version)

        """

        data = {
            'symbol': symbol
        }

        return self._get('open/chart/symbol', False, data=data)

    def get_kline_data_tv(self, symbol, resolution, from_time, to_time):
        """Get kline data (TradingView version)

        """

        data = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time
        }

        return self._get('open/chart/history', False, data=data)

    def get_historical_klines_tv(self, symbol, interval, start_str, end_str=None):
        """Get Historical Klines in OHLCV format (Trading View)
        """

        # init our array for klines
        klines = []

        # convert our date strings to seconds
        if type(start_str) == int:
            start_ts = start_str
        else:
            start_ts = date_to_seconds(start_str)

        # if an end time was not passed we need to use now
        if end_str is None:
            end_str = 'now UTC'
        if type(end_str) == 'int':
            end_ts = end_str
        else:
            end_ts = date_to_seconds(end_str)

        kline_res = self.get_kline_data_tv(symbol, interval, start_ts, end_ts)

        # check if we got a result
        if 't' in kline_res and len(kline_res['t']):
            # now convert this array to OHLCV format and add to the array
            for i in range(1, len(kline_res['t'])):
                klines.append((
                    kline_res['t'][i],
                    kline_res['o'][i],
                    kline_res['h'][i],
                    kline_res['l'][i],
                    kline_res['c'][i],
                    kline_res['v'][i]
                ))

        # finally return our converted klines
        return klines

    def get_coin_info(self, coin):
        """Get info about all coins or a coin
        """

        data = {
            'coin': coin
        }

        return self._get('market/open/coin-info', False, data=data)

    def get_coin_list(self):
        """Get a list of coins with trade and withdrawal information

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-coins(open)

        """

        return self._get('market/open/coins')