"""
Delta.exchange rest cilent
https://docs.delta.exchange
"""
import time
import datetime
import hashlib
import hmac
import json
from enum import Enum
import requests

from decimal import Decimal
from .version import __version__ as version

agent = requests.Session()

url_production = 'https://api.delta.exchange'

agent = requests.Session()

class OrderType(Enum):
    MARKET = 'market_order'
    LIMIT = 'limit_order'


class TimeInForce(Enum):
    FOK = 'fok'
    IOC = 'ioc'
    GTC = 'gtc'

class DeltaRestClient:

    def __init__(self, base_url=url_production, api_key=None, api_secret=None):
        print ("init delta %s %s"%(api_key, api_secret))
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def get_products(self):
        products_url = self.base_url + "/products"
        prd = json.loads(requests.get(products_url).text)
        return prd


    # Check if payload and query are working
    def _request(self, method, path, payload=None, query=None, auth=False):
        url = '%s/%s' % (self.base_url, path)
        if auth:
            if self.api_key is None or self.api_secret is None:
                raise Exception('Api_key or Api_secret missing')
            timestamp = get_time_stamp()
            signature_data = method + timestamp + '/' + path + \
                query_string(query) + body_string(payload)
            signature = generate_signature(self.api_secret, signature_data)
            req_headers = {
                'api-key': self.api_key,
                'timestamp': timestamp,
                'signature': signature,
                'User-Agent': 'rest-client',
                'Content-Type': 'application/json'
            }
        else:
            req_headers = {'User-Agent': 'rest-client'}

        try:
            res = requests.request(
                method, url, data=body_string(payload), params=query, timeout=(3, 27), headers=req_headers
            )

            res.raise_for_status()
            return res
        except Exception as e:
            print ("delta request error: ",e)


    def get_product(self, product_id):
        response = self._request("GET", "products")
        response = response.json()
        products = list(
            filter(lambda x: x['id'] == product_id, response))
        return products[0] if len(products) > 0 else None

    def batch_create(self, product_id, orders):
        response = self._request(
            "POST",
            "orders/batch",
            {'product_id': product_id, 'orders': orders},
            auth=True)
        return response

    def create_order(self, order):
        response = self._request('POST', "orders", order, auth=True)
        return response.json()

    def cancel(self, order):
        print ("cancel ", order)
        try:
            response = self._request(
                "DELETE",
                "orders",
                #{'product_id': order["product_id"], 'orders': orders},
                {'product_id': order["product_id"], 'id': order["id"]},
                auth=True)
        except Exception as e:
            print (e)
        return response.json()

    def batch_cancel(self, product_id, orders):
        print (orders)
        response = self._request(
            "DELETE",
            "orders/batch",
            {'product_id': product_id, 'orders': orders},
            auth=True)
        return response.json()

    def batch_edit(self, product_id, orders):
        response = self._request(
            "PUT",
            "orders/batch",
            {'product_id': product_id, 'orders': orders},
            auth=True
        )
        return response.json()

    def _get_orders_all(self, query=None):
        response = self._request(
            "GET",
            "orders",
            query=query,
            auth=True)
        orders = response.json()
        return orders

    def get_pending_orders(self):
        orders = self._get_orders_all()
        orders = list(filter(lambda o: o["st    ate"] == "pending",orders))        
        return orders
        
    def get_orders(self, query=None):
        orders = self._get_orders_all()
        orders = list(filter(lambda o: o["state"] == "open",orders))        
        return orders

    def get_L2_orders(self, product_id):
        response = self._request("GET", "orderbook/%s/l2" % product_id)
        return response.json()

    def get_ticker(self, product_id):
        l2_orderbook = self.get_L2_orders(product_id)
        best_sell_price = Decimal(l2_orderbook['sell_book'][0]['price']) if len(
            l2_orderbook['sell_book']) > 0 else Decimal('inf')
        best_buy_price = Decimal(l2_orderbook['buy_book'][0]['price']) if len(
            l2_orderbook['buy_book']) > 0 else 0
        return (best_buy_price, best_sell_price)

    def get_summary(self, product_id):
        #r = requests.get('https://api.delta.exchange/products/ticker/24hr', params={
        query = {'symbol': product_id}
        response = self._request("GET","products/ticker/24hr",query=query, auth=True)
        return response.json()

    def get_wallet(self, asset_id):
        response = self._request("GET", "wallet/balance",
                                query={'asset_id': asset_id}, auth=True)
        return response.json()

    def trade_history(self):
        query = {
            'page_num' : 1,
            'page_size' : 100
        }
        response = self._request("GET","orders/history",query=query, auth=True)
        return response.json()


    def get_price_history(self, symbol, duration=5, resolution=1):
        if duration/resolution >= 500:
            raise Exception('Too many Data points')

        current_timestamp = time.mktime(datetime.datetime.today().timetuple())
        last_timestamp = current_timestamp - duration*60
        query = {
            'symbol': symbol,
            'from': last_timestamp,
            'to': current_timestamp,
            'resolution': resolution
        }

        response = self._request("GET", "chart/history", query=query)
        return response.json()

    def get_mark_price(self, product_id):
        response = self._request(
            "GET",
            "orderbook/%s/l2" % product_id)
        response = response.json()
        return float(response['mark_price'])

    def get_leverage(self):
        raise Exception('Method not implemented')

    def close_position(self, product_id):
        response = self._request(
            "POST",
            "positions/close",
            {'product_id': product_id},
            auth=True)
        return response.json()

    def get_positions(self):
        """ get all positions """
        response = self._request(
            "GET",
            "positions",
            auth=True)
        if response:
            response = response.json()            
            return response
        else:
            return []

    def get_position(self, product_id):
        """ get position by product_id """
        position = self.get_positions()
        current_position = list(filter(lambda x: x['product']['id'] == product_id, position))
        return current_position[0] if len(current_position) > 0 else []        

    def set_leverage(self, product_id, leverage):
        response = self._request(
            "POST",
            "orders/leverage",
            {
                'product_id': product_id,
                'leverage':  leverage
            },
            auth=True)
        return response.json()

    def change_position_margin(self, product_id, delta_margin):
        response = self._request(
            'POST',
            'positions/change_margin',
            {
                'product_id': product_id,
                'delta_margin': delta_margin
            },
            auth=True)
        return response.json()

    def order_history(self):
        query = {
            'page_num' : 1,
            'page_size' : 100
        }
        response = self._request("GET","orders/history",query=query, auth=True)
        return response

    def fills(self):
        query = {
            'page_num' : 1,
            'page_size' : 100
        }
        response = self._request("GET","fills",query=query, auth=True)
        return response.json()   


def create_order_format(price, size, side, product_id, post_only='false'):
    order = {
        'product_id': product_id,
        'limit_price': str(price),
        'size': int(size),
        'side': side,
        'order_type': 'limit_order',
        'post_only': post_only
    }

    return order

def create_order_format_post(price, size, side, product_id, post_only='true'):
    order = {
        'product_id': product_id,
        'limit_price': str(price),
        'size': int(size),
        'side': side,
        'order_type': 'limit_order',
        'post_only': post_only
    }

    return order   

def create_order_format_post_buy(price, size, product_id):
    order = create_order_format_post(price, size, "buy", product_id)
    return order

def create_order_format_post_sell(price, size, product_id):
    order = create_order_format_post(price, size, "sell", product_id)
    return order    


def cancel_order_format(x):
    order = {
        'id': x['id'],
        'product_id': x['product']['id']
    }
    return order


def round_by_tick_size(price, tick_size, floor_or_ceil=None):
    remainder = price % tick_size
    if remainder == 0:
        price = price
    if floor_or_ceil == None:
        floor_or_ceil = 'ceil' if (remainder >= tick_size / 2) else 'floor'
    if floor_or_ceil == 'ceil':
        price = price - remainder + tick_size
    else:
        price = price - remainder
    number_of_decimals = len(
        format(Decimal(repr(float(tick_size))), 'f').split('.')[1])
    price = round(Decimal(price), number_of_decimals)
    return price


def generate_signature(secret, message):
    message = bytes(message, 'utf-8')
    secret = bytes(secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest()


def get_time_stamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    return str(int((d - epoch).total_seconds()))


def query_string(query):
    if query == None:
        return ''
    else:
        query_strings = []
        for key, value in query.items():
            query_strings.append(key + '=' + str(value))
        return '?' + '&'.join(query_strings)


def body_string(body):
    if body == None:
        return ''
    else:
        return json.dumps(body, separators=(',', ':'))
