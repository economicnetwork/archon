"""BitMEX API Connector

originally from
https://github.com/BitMEX/easy-data-scripts/

"""
import requests
from time import sleep
import json
from . import errors
import math
import uuid
from .accessTokenAuth import AccessTokenAuth
from .apiKeyAuthWithExpires import APIKeyAuthWithExpires

from loguru import logger

API_BASE = 'https://www.bitmex.com/api/v1/'
# https://www.bitmex.com/api/explorer/

class BitMEX(object):

    """BitMEX REST API"""

    def __init__(self, base_url=API_BASE, symbol=None, login=None, password=None, otpToken=None,
                 apiKey=None, apiSecret=None, orderIDPrefix='mm_bitmex_'):

        logger.start("log/bitmex.log", rotation="500 MB")
        logger.debug("init bitmex")                 
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

    def ticker_data(self):
        """Get ticker data."""
        data = self.get_instrument()

        ticker = {
            # Rounding to tickLog covers up float error
            "last": data['lastPrice'],
            "buy": data['bidPrice'],
            "sell": data['askPrice'],
            "mid": (float(data['bidPrice']) + float(data['askPrice'])) / 2
        }

        return {k: round(float(v), data['tickLog']) for k, v in ticker.items()}

    def get_instrument(self, symbol):
        """Get an instrument's details."""
        path = "instrument"
        instruments = self._query_bitmex(path=path, query={'filter': json.dumps({'symbol': symbol})})
        if len(instruments) == 0:
            logger.error("Instrument not found: %s." % self.symbol)
            #logger.error

        instrument = instruments[0]
        if instrument["state"] != "Open":
            logger.error("The instrument %s is no longer open. State: %s" % (self.symbol, instrument["state"]))
            #logger.error

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
        logger.debug("query ",query)
        result = self._query_bitmex(path=path,query=query)
        return result

    def trades_candle(self, symbol):
        path = "trade/bucketed"
        query = {
            'symbol': symbol,
            'reverse': 'true',
            'count': 100,
            'binSize': '1m', #1m,5m,1h,1d
            #'start': 0,
            #'filter': 
        }
        logger.debug("query ",query)
        result = self._query_bitmex(path=path,query=query)
        return result

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
        logger.debug("query %s"%str(query))
        result = self._query_bitmex(path=path,query=query)
        return result

    @authentication_required
    def position(self):
        """Position : Summary of Open and Closed Positions"""
        return self._query_bitmex(path="position")

    @authentication_required
    def buy(self, symbol, quantity, price):
        """Place a buy order.
        Returns order object. ID: orderID
        """
        #selling is encoded as positive quantities
        directional_quantity = +quantity
        return self.place_order(symbol, directional_quantity, price)

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
        logger.debug("place order. post dict %s"%str(postdict))
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
        logger.debug("place order. post dict %s"%str(postdict))
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

        # Default to POST if data is attached, GET otherwise
        if not verb:
            verb = 'POST' if postdict else 'GET'

        # Auth: Use Access Token by default, API Key/Secret if provided
        auth = AccessTokenAuth(self.token)
        if self.apiKey:
            auth = APIKeyAuthWithExpires(self.apiKey, self.apiSecret)

        # Make the request
        try:
            req = requests.Request(verb, url, data=postdict, auth=auth, params=query)
            prepped = self.session.prepare_request(req)
            response = self.session.send(prepped, timeout=timeout)
            # Make non-200s throw
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            # 401 - Auth error. Re-auth and re-run this request.
            if response.status_code == 401:
                if self.token is None:
                    logger.error("Login information or API Key incorrect, please check and restart.")
                    logger.error("Error: " + response.text)
                    if postdict:
                        logger.error(postdict)
                    #logger.error
                logger.error("Token expired, reauthenticating...")
                sleep(1)
                self.authenticate()
                return self._query_bitmex(path, query, postdict, timeout, verb)

            # 404, can be thrown if order canceled does not exist.
            elif response.status_code == 404:
                if verb == 'DELETE':
                    logger.error("Order not found: %s" % postdict['orderID'])
                    return
                logger.error("Unable to contact the BitMEX API (404). Request: %s \n %s" % (url, json.dumps(postdict)))
                raise Exception("bitmex connection")

            # 503 - BitMEX temporary downtime, likely due to a deploy. Try again
            elif response.status_code == 503:
                logger.error("Unable to contact the BitMEX API (503), retrying. Request: %s \n %s" % (url, json.dumps(postdict)))
                sleep(1)
                return self._query_bitmex(path, query, postdict, timeout, verb)
            # Unknown Error
            else:
                logger.error("Unhandled Error: %s %s"%(str(e), str(response.text)))
                logger.error("Endpoint was: %s %s" % (verb, path))
                raise Exception("bitmex connection")

        except requests.exceptions.Timeout as e:
            # Timeout, re-run this request
            logger.error("Timed out, retrying...")
            return self._query_bitmex(path, query, postdict, timeout, verb)

        except requests.exceptions.ConnectionError as e:
            logger.error("Unable to contact the BitMEX API (ConnectionError). Please check the URL. Retrying. Request: %s \n %s" % (url, json.dumps(postdict)))
            sleep(1)
            return self._query_bitmex(path, query, postdict, timeout, verb)

        return response.json()