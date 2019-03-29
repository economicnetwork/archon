# coding: utf-8

from __future__ import absolute_import
import requests
import json
import base64
import hmac
import hashlib
import time
import logging
import urllib
import urllib.parse


PROTOCOL = "https"
HOST = "www.okex.com/api"
VERSION = "v1"

PATH_SYMBOLS = "symbols"     #获取支持的币币交易类型
PATH_TICKER = "ticker.do"    #获取币币交易行情
PATH_TRADES = "trades.do"    #获取币币交易信息
PATH_DEPTH = "depth.do"      #获取币币市场深度
PATH_ORDER_INFO = "order_info.do"   #获取订单信息
PATH_ORDERS_INFO = "orders_info.do"   #批量获取订单信息
PATH_ORDER_HISTORY = "order_history.do"   #获取历史订单信息，只返回最近两天的信息
PATH_CANCEL_ORDER = "cancel_order.do"   #撤销订单
PATH_BALANCES_USERINFO = "userinfo.do"  #个人资产情况
PATH_TRADE = "trade.do"    #获取币币交易信息

# HTTP request timeout in seconds
TIMEOUT = 10.0


class OkexClientError(Exception):
    pass


class OkexBaseClient(object):
    def __init__(self, key, secret, proxies=None):
        self.URL = "{0:s}://{1:s}/{2:s}".format(PROTOCOL, HOST, VERSION)
        self.KEY = key
        self.SECRET = secret
        self.PROXIES = proxies

    @property
    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(time.time() * 1000))

    def _build_parameters(self, parameters):
        # sort the keys so we can test easily in Python 3.3 (dicts are not
        # ordered)
        keys = list(parameters.keys())
        keys.sort()
        return '&'.join(["%s=%s" % (k, parameters[k]) for k in keys])

    def url_for(self, path, path_arg=None, parameters=None):
        url = "%s/%s" % (self.URL, path)
        # If there is a path_arh, interpolate it into the URL.
        # In this case the path that was provided will need to have string
        # interpolation characters in it
        if path_arg:
            url = url % (path_arg)
        # Append any parameters to the URL.
        if parameters:
            url = "%s?%s" % (url, self._build_parameters(parameters))
        return url

    def _sign_payload(self, payload):
        sign = ''
        for key in sorted(payload.keys()):
            sign += key + '=' + str(payload[key]) +'&'
        data = sign+'secret_key='+self.SECRET
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()

    def _convert_to_floats(self, data):
        """
        Convert all values in a dict to floats at first level
        """
        for key, value in data.items():
            data[key] = float(value)
        return data

    def _get(self, url, timeout=TIMEOUT):
        req = requests.get(url, timeout=timeout, proxies=self.PROXIES)
        if req.status_code/100 != 2:
            logging.error(u"Failed to request:%s %d headers:%s", url, req.status_code, req.headers)
        try:
            return req.json()
        except Exception as e:
            logging.exception('Failed to GET:%s result:%s', url, req.text)
            raise e

    def _post(self, url, params=None, needsign=True, headers=None, timeout=TIMEOUT):
        req_params = {'api_key' : self.KEY}
        print (self.KEY)
        if params and needsign:
            req_params.update(params)
        print (req_params)
        signature = self._sign_payload(req_params)
        print (signature)
        req_params['sign'] = signature
        
        req_headers = {
            "Content-type" : "application/x-www-form-urlencoded",
        }
        if headers:
            req_headers.update(headers)
        logging.info("%s %s", req_headers, req_params)

        #req = requests.post(url, headers=req_headers, data=urllib.parse.urlencode(req_params), timeout=TIMEOUT, proxies=self.PROXIES)
        req = requests.post(url, headers=req_headers, data=urllib.parse.urlencode(req_params), timeout=TIMEOUT)
        if req.status_code/100 != 2:
            logging.error(u"Failed to request:%s %d headers:%s", url, req.status_code, req.headers)
        try:
            return req.json()
        except Exception as e:
            logging.exception('Failed to POST:%s result:%s', url, req.text)
            raise e


class OkexTradeClient(OkexBaseClient):
    """
    Authenticated client for trading through Bitfinex API
    """

    def place_order(self, amount, price, ord_type, symbol='btcusd'):
        """
        # Request
        POST https://www.okex.com/api/v1/trade.do
        # Response
        {"result":true,"order_id":123456}
        """
        assert(isinstance(amount, str) and isinstance(price, str))

        if ord_type not in ('buy', 'sell', 'buy_market', 'sell_market'):
            #买卖类型： 限价单（buy/sell） 市价单（buy_market/sell_market）
            raise OkexClientError("Invaild order type")

        payload = {
            "symbol": symbol, "amount": amount, "price": price, "type": ord_type
        }
        result = self._post(self.url_for(PATH_TRADE), params=payload)
        if 'error_code' not in result and result['result'] and result['order_id']:
            return result
        raise OkexClientError('Failed to place order:'+str(result))

    def status_order(self, symbol, order_id):
        """
        # Request
        order_id -1:未完成订单，否则查询相应订单号的订单
        POST https://www.okex.com/api/v1/order_info.do
        # Response
        {
            "result": true,
            "orders": [
                {
                    "amount": 0.1,
                    "avg_price": 0,
                    "create_date": 1418008467000,
                    "deal_amount": 0,
                    "order_id": 10000591,
                    "orders_id": 10000591,
                    "price": 500,
                    "status": 0,
                    "symbol": "btc_usd",
                    "type": "sell"
                }
            ]
        }
        amount:委托数量
        create_date: 委托时间
        avg_price:平均成交价
        deal_amount:成交数量
        order_id:订单ID
        orders_id:订单ID(不建议使用)
        price:委托价格
        status:-1:已撤销  0:未成交  1:部分成交  2:完全成交 4:撤单处理中
        type:buy_market:市价买入 / sell_market:市价卖出
        """
        payload = {
            "symbol": symbol, "order_id": order_id
        }
        result = self._post(self.url_for(PATH_ORDER_INFO), params=payload)
        if result['result']:
            return result
        raise OkexClientError('Failed to get order status:'+str(result))

    def cancel_order(self, symbol, order_id):
        '''
        # Request
        POST https://www.okex.com/api/v1/cancel_order.do
        order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消3个订单)
        # Response
        #多笔订单返回结果(成功订单ID,失败订单ID)
        {"success":"123456,123457","error":"123458,123459"}
        '''
        payload = {
            "symbol": symbol, "order_id": order_id
        }
        result = self._post(self.url_for(PATH_CANCEL_ORDER), params=payload)
        if result['result']:
            return result
        raise OkexClientError('Failed to cancal order:%s %s' % (symbol, order_id))

    def cancel_orders(self, symbol, order_ids):
        final_result = {'result':True, 'success':[], 'error':[]}
        for i in range(0, len(order_ids), 3):
            three_order_ids = ",".join(order_ids[i:i+3])
            tmp = self.cancel_order(symbol, three_order_ids)
            final_result['result'] &= tmp['result']
            final_result['success'].extend(tmp['success'].split(','))
            final_result['error'].extend(tmp['error'].split(','))
        return final_result

    def active_orders(self, symbol):
        """
        Fetch active orders
        """
        return self.status_order(symbol, -1)

    def history(self, symbol, status, limit=500):
        """
        # Request
        POST https://www.okex.com/api/v1/order_history.do
        status: 查询状态 0：未完成的订单 1：已经完成的订单 （最近两天的数据）
        # Response
        {
            "current_page": 1,
            "orders": [
                {
                    "amount": 0,
                    "avg_price": 0,
                    "create_date": 1405562100000,
                    "deal_amount": 0,
                    "order_id": 0,
                    "price": 0,
                    "status": 2,
                    "symbol": "btc_usd",
                    "type": "sell”
                }
            ],
            "page_length": 1,
            "result": true,
            "total": 3
        }
        status:-1:已撤销   0:未成交 1:部分成交 2:完全成交 4:撤单处理中
        type:buy_market:市价买入 / sell_market:市价卖出
        """
        PAGE_LENGTH = 200 # Okex限制 每页数据条数，最多不超过200
        final_result = []
        for page_index in range(int(limit/PAGE_LENGTH)+1):
            payload = {
                "symbol": symbol,
                "status": status,
                "current_page": page_index,
                "page_length": PAGE_LENGTH,
            }
            result = self._post(self.url_for(PATH_ORDER_HISTORY), params=payload)
            if not result['result']:
                raise OkexClientError('Failed to get history order:%s %s' % (symbol, result))
            if len(result['orders'])>0:
                final_result.extend(result['orders'])
            else:
                break
        return final_result

    def balances(self):
        '''
        # Request
        POST https://www.okex.com/api/v1/userinfo.do
        # Response
        {
            "info": {
                "funds": {
                    "free": {
                        "btc": "0",
                        "usd": "0",
                        "ltc": "0",
                        "eth": "0"
                    },
                    "freezed": {
                        "btc": "0",
                        "usd": "0",
                        "ltc": "0",
                        "eth": "0"
                    }
                }
            },
            "result": true
        }
        '''
        payload = {
        }
        print (self.url_for(PATH_BALANCES_USERINFO))
        result = self._post(self.url_for(PATH_BALANCES_USERINFO), params=payload)
        print (result)
        if result['result']:
            return result
        raise OkexClientError('Failed to get balances userinfo order:%s' % result)


class OkexClient(OkexBaseClient):
    """
    Client for the Okex.com API.
    See https://www.okex.com/rest_api.html for API documentation.
    """

    def ticker(self, symbol):
        """
        GET /api/v1/ticker.do?symbol=ltc_btc

        GET https://www.okex.com/api/v1/ticker.do?symbol=ltc_btc
        {
            "date":"1410431279",
            "ticker":{
                "buy":"33.15",
                "high":"34.15",
                "last":"33.15",
                "low":"32.05",
                "sell":"33.16",
                "vol":"10532696.39199642"
            }
        }
        """
        return self._get(self.url_for(PATH_TICKER, parameters={'symbol' : symbol}))

    def trades(self, symbol, since_tid=None):
        """
        GET /api/v1/trades.do
        GET https://www.okex.com/api/v1/trades.do?symbol=ltc_btc&since=7622718804
        [
            {
                "date": "1367130137",
                "date_ms": "1367130137000",
                "price": 787.71,
                "amount": 0.003,
                "tid": "230433",
                "type": "sell"
            }
        ]
        """
        params = {'symbol':symbol}
        if since_tid:
            params['since'] = since_tid
        return self._get(self.url_for(PATH_TRADES, parameters=params))

    def depth(self, symbol, size=200):
        '''
        # Request
        GET https://www.okex.com/api/v1/depth.do?symbol=ltc_btc
        # Response
        {
            "asks": [
                [792, 5],
                [789.68, 0.018],
                [788.99, 0.042],
                [788.43, 0.036],
                [787.27, 0.02]
            ],
            "bids": [
                [787.1, 0.35],
                [787, 12.071],
                [786.5, 0.014],
                [786.2, 0.38],
                [786, 3.217],
                [785.3, 5.322],
                [785.04, 5.04]
            ]
        }
        '''
        params = {'symbol':symbol}
        if size>0:
            params['size'] = size
        return self._get(self.url_for(PATH_DEPTH, parameters=params))
