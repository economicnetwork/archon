"""
BitMEX API
https://www.bitmex.com/app/restAPI
https://www.bitmex.com/api/explorer/

originally from https://github.com/BitMEX/easy-data-scripts/
* added time-out handling
* candle request methods

"""
import requests
from time import sleep
import json
from . import errors
import math
import uuid
from .accessTokenAuth import AccessTokenAuth
from .apiKeyAuthWithExpires import APIKeyAuthWithExpires

from archon.util.custom_logger import setup_logger
import datetime
from datetime import timedelta
import logging
import time

API_BASE = 'https://www.bitmex.com/api/v1/'
# https://www.bitmex.com/api/explorer/

candle_1m = '1m'
candle_5m = '5m'
candle_1h = '1h'
candle_1d = '1d'

instrument_btc_perp = "XBTUSD"
instrument_btc_mar19 = "XBTH19"
instrument_btc_jun19 = "XBTM19"

class ConnectionError(Exception):
    def __init__(self, message): #, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # custom code...
        #self.errors = errors

class BitMEX(object):

    """BitMEX REST API"""

    def __init__(self, base_url=API_BASE, symbol=None, login=None, password=None, otpToken=None,
                 apiKey=None, apiSecret=None, orderIDPrefix='mm_bitmex_'):

        setup_logger(logger_name=__name__, log_file='bitmex.log')
        self.logger = logging.getLogger(__name__)
        self.logger.info("init bitmex")
        self.base_url = base_url
        self.symbol = symbol
        self.token = None
        self.login = login
        self.password = password
        self.otpToken = otpToken
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        if len(orderIDPrefix) > 13:
            raise ValueError("settings.ORDERID_PREFIX must be at most 13 characters long!")
        self.orderIDPrefix = orderIDPrefix

        # Prepare HTTPS session
        self.session = requests.Session()
        # These headers are always sent
        self.session.headers.update({'user-agent': 'easy-data-scripts'})

    # --- Public methods ---

    def ticker_data(self, symbol):
        """Get ticker data."""
        data = self.get_instrument(symbol)
        #print(data)
        #print (data.keys())

        v = data['volume24h']
        last = data['lastPrice']
        usd_volume = v*last
        #print (symbol, usd_volume)

        ticker = {
            # Rounding to tickLog covers up float error
            "last": last,
            "bid": data['bidPrice'],
            "ask": data['askPrice'],
            "mid": (float(data['bidPrice']) + float(data['askPrice'])) / 2,
            "volume24h": v
        }

        #rounded = {k: round(float(v), data['tickLog']) for k, v in ticker.items()}
        #print (rounded["buy"])
        #print (rounded["sell"])
        return ticker

    def get_active_instruments(self):
        """Get all instrument's details."""
        path = "instrument/active"
        instruments = self._query_bitmex(path=path, query={})
        return instruments

    def get_instruments(self, symbol):
        """Get all instrument's details."""
        path = "instrument"
        instruments = self._query_bitmex(path=path, query={})
        print (instruments)


    def get_instrument(self, symbol):
        """Get an instrument's details."""
        path = "instrument"
        instruments = self._query_bitmex(path=path, query={'filter': json.dumps({'symbol': symbol})})
        if len(instruments) == 0:
            self.logger.error("Instrument not found: %s." % self.symbol)
            #self.logger.error

        instrument = instruments[0]
        if instrument["state"] != "Open":
            self.logger.error("The instrument %s is no longer open. State: %s" % (self.symbol, instrument["state"]))
            #self.logger.error

        # tickLog is the log10 of tickSize
        instrument['tickLog'] = int(math.fabs(math.log10(instrument['tickSize'])))

        return instrument

    def market_depth(self, symbol, depth=0):
        """Get market depth / orderbook."""
        path = "orderBook/L2"
        #https://www.bitmex.com/api/v1/orderBook/L2?symbol=XBTUSD&depth=0
        result = self._query_bitmex(path=path, query={'symbol': symbol, 'depth': depth})
        return result

    def recent_trades(self, symbol):
        """Get recent trades.

        Returns
        -------
        A list of dicts:
              {u'amount': 60,
               u'date': 1306775375,
               u'price': 8.7401099999999996,
               u'tid': u'93842'},

        """
        path = "trade"
        query = {
            'symbol': symbol,
            'reverse': 'true',
            'count': 100
            #'start': 0,
            #'filter': 
        }
        self.logger.debug("query ",query)
        result = self._query_bitmex(path=path,query=query)
        return result

    def trades_candle(self, symbol, resolution, count=100, startTime=None, endTime=None):
        path = "trade/bucketed"
        query = {
            'symbol': symbol,
            'reverse': 'true',
            'count': count,
            'binSize': resolution            
            #'start': 0,
            #'filter': 
        }
        if startTime:
            query['startTime'] = startTime
        if endTime:
            query['endTime'] = endTime

        self.logger.debug("query ",query)
        result = self._query_bitmex(path=path,query=query)
        return result

    def get_minute_1day(self, startday):
        """ gets 1m data for a single day . split request in two because maximum candles per request is 750 """
        maxrequest = 750
        startTime = startday
        endTime = startTime + timedelta(hours=12)
        candles = self.trades_candle("XBTUSD", candle_1m, maxrequest, startTime, endTime)
        candles.reverse()

        #add second half of the day
        startTime = endTime
        endTime = startTime + timedelta(hours=12)
        candles2 = self.trades_candle("XBTUSD", candle_1m, maxrequest, startTime, endTime)
        candles2.reverse()

        candles += candles2

        return candles

    def history(self, start):
        n = datetime.datetime.now()
        start_day = datetime.datetime(start.year, start.month, start.day)
        cur = start_day
        all_candles = list()

        while cur < n:
            cur += timedelta(hours=24)
            self.logger.debug("fetch %s"%str(cur))
            d = self.get_minute_1day(cur)
            all_candles += d
        return all_candles

    def history_days(self, numdays):
        n = datetime.datetime.now()
        start = n - datetime.timedelta(days=numdays)
        candles = self.history(start)
        return candles
        



    @property
    def snapshot(self):
        """Get current BBO."""
        order_book = self.market_depth()
        return {
            'bid': order_book[0]['bidPrice'],
            'ask': order_book[0]['askPrice'],
            'size_bid': order_book[0]['bidSize'],
            'size_ask': order_book[0]['askSize']
        }

    # --- Authentication required methods ---

    def authenticate(self):
        """Set BitMEX authentication information."""
        if self.apiKey:
            return
        loginResponse = self._query_bitmex(
            path="user/login",
            postdict={'email': self.login, 'password': self.password, 'token': self.otpToken})
        self.token = loginResponse['id']
        self.session.headers.update({'access-token': self.token})

    def authentication_required(fn):
        """Annotation for methods that require auth."""
        def wrapped(self, *args, **kwargs):
            if not (self.token or self.apiKey):
                msg = "You must be authenticated to use this method"
                raise errors.AuthenticationError(msg)
            else:
                return fn(self, *args, **kwargs)
        return wrapped

    @authentication_required
    def funds(self):
        """Get your current balance."""
        return self._query_bitmex(path="user/margin")

    def execution_history(self, symbol, timestamp):
        """ all orders including non-executed """
        
        #path = "user/executionHistory" 
        #['execID', 'orderID', 'clOrdID', 'clOrdLinkID', 'account', 'symbol', 'side', 'lastQty', 'lastPx', 'underlyingLastPx', 
        # 'lastMkt', 'lastLiquidityInd', 'simpleOrderQty', 'orderQty', 'price', 'displayQty', 'stopPx', 'pegOffsetValue',
        #  'pegPriceType', 'currency', 'settlCurrency', 'execType', 'ordType', 'timeInForce', 'execInst', 'contingencyType', 
        # 'exDestination', 'ordStatus', 'triggered', 'workingIndicator', 'ordRejReason', 'simpleLeavesQty', 'leavesQty', 
        # 'simpleCumQty', 'cumQty', 'avgPx', 'commission', 'tradePublishIndicator', 'multiLegReportingType', 'text', 
        # 'trdMatchID', 'execCost', 'execComm', 'homeNotional', 'foreignNotional', 'transactTime', 'timestamp']       
        path = "execution"        
        query = {
            'symbol': symbol,
            'timestamp': timestamp,
            #'reverse': 'true'
            #'count': 100
            #'start': 0,
            #'filter': 
        }
        self.logger.debug("query %s"%str(query))
        result = self._query_bitmex(path=path,query=query)
        return result

    def execution_history_all(self, symbol):
        now = datetime.datetime.now()
        #TODO
        from_ts = "2019-01-13T12:00:00.000Z"
        prev = now.strftime("%Y-%m-%dT12:00:00.000Z")
        print (prev)
        tx = self.execution_history(symbol, prev)
        return tx
        #startTime = startday
        #endTime = startTime + timedelta(hours=12)
        

    def funding(self, starttime):
        symbol = instrument_btc_perp
        query = {
            'symbol': symbol,
            'startTime': starttime,
            'count': 500
            #,
            #'timestamp': timestamp,
            #'reverse': 'true'
            #'count': 100
            #'start': 0,
            #'filter': 
        }
        return self._query_bitmex(path="funding", query=query)

    @authentication_required
    def position(self):
        """Position : Summary of Open and Closed Positions"""
        return self._query_bitmex(path="position")

    @authentication_required
    def buy(self, symbol, quantity, price):
        """Place a buy order. 
        Returns order object. ID: orderID"""
        #selling is encoded as positive quantities
        directional_quantity = +quantity
        result = self.place_order(symbol, directional_quantity, price)
        self.logger.debug("order result %s"%str(result))
        return result

    @authentication_required
    def buy_post(self, symbol, quantity, price):
        """Place a buy order.
        Returns order object. ID: orderID
        """
        #selling is encoded as positive quantities
        directional_quantity = +quantity
        return self.place_order_post(symbol, directional_quantity, price)        

    @authentication_required
    def sell(self, symbol, quantity, price):
        """Place a sell order.
        Returns order object. ID: orderID
        """
        #selling is encoded as negative quantities
        directional_quantity = -quantity
        return self.place_order(symbol, directional_quantity, price)

    @authentication_required
    def sell_post(self, symbol, quantity, price):
        """Place a sell order.
        Returns order object. ID: orderID
        """
        #selling is encoded as negative quantities
        directional_quantity = -quantity
        return self.place_order_post(symbol, directional_quantity, price)

    @authentication_required
    def place_order(self, symbol, quantity, price):
        """Place an order."""
        if price < 0:
            raise Exception("Price must be positive.")

        endpoint = "order"
        # Generate a unique clOrdID with our prefix so we can identify it.
        #AttributeError: 'bytes' object has no attribute 'encode'
        #clOrdID = self.orderIDPrefix + uuid.uuid4().bytes.encode('base64').rstrip('=\n')
        clOrdID = uuid.uuid4()
        postdict = {
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'clOrdID': clOrdID
        }
        self.logger.debug("place order. post dict %s"%str(postdict))
        return self._query_bitmex(path=endpoint, postdict=postdict, verb="POST")

    @authentication_required
    def place_order_post(self, symbol, quantity, price):
        """Place an order with post only"""
        if price < 0:
            raise Exception("Price must be positive.")

        endpoint = "order"
        # Generate a unique clOrdID with our prefix so we can identify it.
        #AttributeError: 'bytes' object has no attribute 'encode'
        #clOrdID = self.orderIDPrefix + uuid.uuid4().bytes.encode('base64').rstrip('=\n')
        clOrdID = uuid.uuid4()
        postdict = {
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'clOrdID': clOrdID,
            'execInst': 'ParticipateDoNotInitiate'
        }
        self.logger.debug("place order. post dict %s"%str(postdict))
        return self._query_bitmex(path=endpoint, postdict=postdict, verb="POST")        

    @authentication_required
    def open_orders(self, symbol):
        """Get open orders."""
        path = "order"

        filter_dict = {'ordStatus.isTerminated': False}
        #if self.symbol:
        #    filter_dict['symbol'] = self.symbol

        orders = self._query_bitmex(
            path=path,
            query={'filter': json.dumps(filter_dict)},
            verb="GET"
        )
        # Only return orders that start with our clOrdID prefix.
        #orders = [o for o in orders if str(o['clOrdID']).startswith(self.orderIDPrefix)]
        return orders

    @authentication_required
    def cancel(self, orderID):
        """Cancel an existing order."""
        path = "order"
        postdict = {
            'orderID': orderID,
        }
        cancel_result = self._query_bitmex(path=path, postdict=postdict, verb="DELETE")

        return cancel_result


    def _query_bitmex(self, path, query=None, postdict=None, timeout=3, verb=None):
        """Send a request to BitMEX Servers."""                
        # Handle URL
        url = self.base_url + path
        #self.logger.debug("query %s"%str(url))

        # Default to POST if data is attached, GET otherwise
        if not verb:
            verb = 'POST' if postdict else 'GET'

        # Auth: Use Access Token by default, API Key/Secret if provided
        auth = AccessTokenAuth(self.token)
        if self.apiKey:
            #self.logger.debug("got api key")
            auth = APIKeyAuthWithExpires(self.apiKey, self.apiSecret)

        # Make the request
        try:
            #self.logger.debug("query verb %s url %s data %s query %s"%(str(verb),str(url),str(postdict),str(query)))
            #self.logger.debug("auth %s"%str(auth))
            req = requests.Request(verb, url, data=postdict, auth=auth, params=query)
            prepped = self.session.prepare_request(req)
            response = self.session.send(prepped, timeout=timeout)
            # Make non-200s throw
            response.raise_for_status()
            h = response.headers
            #self.logger.debug("header %s"%str(h))
            remain = int(h['X-RateLimit-Remaining'])
            #self.logger.debug("remain %i"%remain)
            if remain < 100: time.sleep(0.2)

        except requests.exceptions.HTTPError as e:
            # 401 - Auth error. Re-auth and re-run this request.
            if response.status_code == 401:
                if self.token is None:
                    self.logger.error("Login information or API Key incorrect, please check and restart.")
                    self.logger.error("Error: " + response.text)
                    if postdict:
                        self.logger.error(postdict)
                    #self.logger.error
                self.logger.error("Token expired, reauthenticating...")
                sleep(1)
                self.authenticate()
                return self._query_bitmex(path, query, postdict, timeout, verb)
            elif response.status_code == 403:
                self.logger.error("403 error")
                h = response.headers
                self.logger.error("Unhandled Error: %s %s"%(str(e), str(response.text)))
                self.logger.error("Endpoint was: %s %s" % (verb, path))
                self.logger.error("headers %s"%(str(h)))
                #raise Exception("bitmex connection error")
                raise ConnectionError("bitmex error")


            # 404, can be thrown if order canceled does not exist.
            elif response.status_code == 404:
                if verb == 'DELETE':
                    self.logger.error("Order not found: %s" % postdict['orderID'])
                    return
                self.logger.error("Unable to contact the BitMEX API (404). Request: %s \n %s" % (url, json.dumps(postdict)))
                raise ConnectionError("bitmex error. order canceled does not exist.")
            elif response.status_code == 429:
                 #Unhandled Error: 429 Client Error: Too Many Requests for url... {"error":{"message":"Rate limit exceeded, retry in 1 seconds.","name":"RateLimitError"}}
                 #self.logger.error("429 Too Many Requests for url. Request: %s \n %s" % (url, json.dumps(postdict)))
                 self.logger.error("429 Too Many Requests for url. Request: %s" % url)
                 h = response.headers
                 
                 self.logger.error("headers %s"%str(h))
                 retry = int(h["Retry-After"])
                 remain = int(h["X-RateLimit-Remaining"])
                 #'X-RateLimit-Remaining': '0', 
                 reset = int(h['X-RateLimit-Reset'])
                 nt =  int(time.time())
                 wait_for = reset - nt
                 time.sleep(wait_for)
                 self.logger.error("wait for %i"%wait_for)
                 return self._query_bitmex(path, query, postdict, timeout, verb)
            # 503 - BitMEX temporary downtime, likely due to a deploy. Try again
            elif response.status_code == 503:
                #self.logger.error("Unable to contact the BitMEX API (503), retrying. Request: %s \n %s" % (url, json.dumps(postdict)))
                self.logger.error("Unable to contact the BitMEX API (503), retrying. Request: %s" % url)
                sleep(1)
                return self._query_bitmex(path, query, postdict, timeout, verb)            
            # Unknown Error
            #TODO Timeouts?
            else:
                self.logger.error("Unhandled Error: %s %s"%(str(e), str(response.text)))
                self.logger.error("Endpoint was: %s %s" % (verb, path))
                #raise Exception("bitmex connection error")
                raise ConnectionError("bitmex error")

        except requests.exceptions.Timeout as e:
            # Timeout, re-run this request
            self.logger.error("Timed out, retrying...")
            time.sleep(0.5)
            return self._query_bitmex(path, query, postdict, timeout, verb)

        except requests.exceptions.ConnectionError as e:
            #self.logger.error("Unable to contact the BitMEX API (ConnectionError). Please check the URL. Retrying. Request: %s \n %s" % (url, json.dumps(postdict)))
            self.logger.error("Unable to contact the BitMEX API (ConnectionError). Please check the URL. Retrying. Request: %s" % url)
            sleep(1)
            return self._query_bitmex(path, query, postdict, timeout, verb)

        return response.json()