import websocket
import threading
import traceback
from time import sleep
import json
import logging
import urllib
import math
import time, urllib, hmac, hashlib


def generate_nonce():
    return int(round(time.time() + 3600))


# Generates an API signature.
# A signature is HMAC_SHA256(secret, verb + path + nonce + data), hex encoded.
# Verb must be uppercased, url is relative, nonce must be an increasing 64-bit integer
# and the data, if present, must be JSON without whitespace between keys.

def generate_signature(secret, verb, url, nonce, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urllib.parse.urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    # print "Computing HMAC: %s" % verb + path + str(nonce) + data
    message = (verb + path + str(nonce) + data).encode('utf-8')

    signature = hmac.new(secret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    return signature



# Naive implementation of connecting to BitMEX websocket for streaming realtime data.

# The Websocket offers a bunch of data as raw properties right on the object.
# On connect, it synchronously asks for a push of all this data then returns.

class BitMEXWebsocket:

    # Don't grow a table larger than this amount. Helps cap memory usage.
    MAX_TABLE_LEN = 200

    def __init__(self, endpoint, symbol, api_key=None, api_secret=None):
        '''Connect to the websocket and initialize data stores.'''
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing WebSocket.")

        self.endpoint = endpoint
        self.symbol = symbol

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')

        self.api_key = api_key
        self.api_secret = api_secret

        self.data = {}
        self.keys = {}
        self.exited = False
        self.msg_count = 0

        self.orderbook = {}

        

    def start_ws_thread(self):
        # We can subscribe right in the connection querystring, so let's build that.
        # Subscribe to all pertinent endpoints
        wsURL = self.__get_url()
        self.logger.info("Connecting to %s" % wsURL)
        self.__connect(wsURL, self.symbol)
        self.logger.info('Connected to WS.')

        #TODO cleanup
        # Connected. Wait for partials
        self.__wait_for_symbol(self.symbol)
        if self.api_key:
            self.__wait_for_account()
        self.logger.info('Got all market data. Starting.')
        
    def exit(self):
        '''Call this to exit - will close websocket.'''
        self.exited = True
        self.ws.close()

    def get_instrument(self):
        '''Get the raw instrument data for this symbol.'''
        # Turn the 'tickSize' into 'tickLog' for use in rounding
        instrument = self.data['instrument'][0]
        instrument['tickLog'] = int(math.fabs(math.log10(instrument['tickSize'])))
        return instrument

    def get_ticker(self):
        '''Return a ticker object. Generated from quote and trade.'''
        lastQuote = self.data['quote'][-1]
        lastTrade = self.data['trade'][-1]
        ticker = {
            "last": lastTrade['price'],
            "buy": lastQuote['bidPrice'],
            "sell": lastQuote['askPrice'],
            "mid": (float(lastQuote['bidPrice'] or 0) + float(lastQuote['askPrice'] or 0)) / 2
        }

        # The instrument has a tickSize. Use it to round values.
        instrument = self.data['instrument'][0]
        return {k: round(float(v or 0), instrument['tickLog']) for k, v in ticker.items()}

    def funds(self):
        '''Get your margin details.'''
        return self.data['margin'][0]

    def positions(self):
        '''Get your positions.'''
        return self.data['position']

    def market_depth(self):
        '''Get market depth (orderbook). Returns all levels.'''
        return self.data['orderBookL2']

    def open_orders(self, clOrdIDPrefix):
        '''Get all your open orders.'''
        orders = self.data['order']
        # Filter to only open orders and those that we actually placed
        return [o for o in orders if str(o['clOrdID']).startswith(clOrdIDPrefix) and order_leaves_quantity(o)]

    def recent_trades(self):
        '''Get recent trades.'''
        return self.data['trade']

    #
    # End Public Methods
    #

    def __connect(self, wsURL, symbol):
        '''Connect to the websocket in a thread.'''
        self.logger.debug("Starting thread")

        self.ws = websocket.WebSocketApp(wsURL,
                                         on_message=self.__on_message,
                                         on_close=self.__on_close,
                                         on_open=self.__on_open,
                                         on_error=self.__on_error,
                                         header=self.__get_auth())

        self.wst = threading.Thread(target=lambda: self.ws.run_forever())
        self.wst.daemon = True
        self.wst.start()
        self.logger.debug("Started thread")

        # Wait for connect before continuing
        conn_timeout = 5
        while not self.ws.sock or not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        if not conn_timeout:
            self.logger.error("Couldn't connect to WS! Exiting.")
            self.exit()
            raise websocket.WebSocketTimeoutException('Couldn\'t connect to WS! Exiting.')

    def __get_auth(self):
        '''Return auth headers. Will use API Keys if present in settings.'''
        if self.api_key:
            self.logger.info("Authenticating with API Key.")
            # To auth to the WS using an API key, we generate a signature of a nonce and
            # the WS API endpoint.
            expires = generate_nonce()
            return [
                "api-expires: " + str(expires),
                "api-signature: " + generate_signature(self.api_secret, 'GET', '/realtime', expires, ''),
                "api-key:" + self.api_key
            ]
        else:
            self.logger.info("Not authenticating.")
            return []

    def __get_url(self):
        '''
        Generate a connection URL. We can define subscriptions right in the querystring.
        Most subscription topics are scoped by the symbol we're listening to.
        '''

        # You can sub to orderBookL2 for all levels, or orderBook10 for top 10 levels & save bandwidth
        #symbolSubs = ["execution", "instrument", "order", "orderBookL2", "position", "quote", "trade"]
        #TODO
        #symbolSubs = ["orderBookL2"]
        symbolSubs = ["orderBook10"]
        genericSubs = ["margin"]

        subscriptions = [sub + ':' + self.symbol for sub in symbolSubs]
        subscriptions += genericSubs

        print ("subscribe to ", subscriptions)

        urlParts = list(urllib.parse.urlparse(self.endpoint))
        urlParts[0] = urlParts[0].replace('http', 'ws')
        urlParts[2] = "/realtime?subscribe={}".format(','.join(subscriptions))
        return urllib.parse.urlunparse(urlParts)

    def __wait_for_account(self):
        '''On subscribe, this data will come down. Wait for it.'''
        # Wait for the keys to show up from the ws
        while not {'margin', 'position', 'order', 'orderBookL2'} <= set(self.data):
            sleep(0.1)

    def __wait_for_symbol(self, symbol):
        '''On subscribe, this data will come down. Wait for it.'''
        while not {'instrument', 'trade', 'quote'} <= set(self.data):
            sleep(0.1)

    def __send_command(self, command, args=None):
        '''Send a raw command.'''
        if args is None:
            args = []
        self.ws.send(json.dumps({"op": command, "args": args}))

    #----------------------------------------------------------------
    # custom handlers
    #----------------------------------------------------------------

    def handle_paritial(self, table, message):
        #print (message)
        self.logger.debug("%s: partial" % table)
        self.data[table] = message['data']
        # Keys are communicated on partials to let you know how to uniquely identify
        # an item. We use it for updates.
        self.keys[table] = message['keys']

    def handle_insert(self, table, message):
        self.logger.debug('%s: inserting %s' % (table, message['data']))
        self.data[table] += message['data']

        # Limit the max length of the table to avoid excessive memory usage.
        # Don't trim orders because we'll lose valuable state if we do.
        #if table not in ['order', 'orderBookL2'] and len(self.data[table]) > BitMEXWebsocket.MAX_TABLE_LEN:
        #    self.data[table] = self.data[table][BitMEXWebsocket.MAX_TABLE_LEN // 2:]

    def handle_update(self, table, message):
        d = message['data']
        print (d)

        self.logger.info('%s: updating %s' % (table, message['data']))
        # Locate the item in the collection and update it.        
        for updateData in d:
            item = find_by_keys(self.keys[table], self.data[table], updateData)
            if not item:
                return  # No item found to update. Could happen before push
            item.update(updateData)

            # Remove cancelled / filled orders
            if table == 'order' and not order_leaves_quantity(item):
                self.data[table].remove(item)

    def handle_delete(self, table, message):
        self.logger.debug('%s: deleting %s' % (table, message['data']))
        # Locate the item in the collection and remove it.
        for deleteData in message['data']:
            item = find_by_keys(self.keys[table], self.data[table], deleteData)
            self.data[table].remove(item)

    def mid_price(self):
        d = self.orderbook
        bids,asks = d['bids'],d['asks']
        topbid = bids[0][0]
        topask = asks[0][0]
        mid = (topbid + topask)/2
        return mid
        #print (topbid, topask, mid)

    def hanldle_book10(self, message):
        d = message['data'][0]

        self.orderbook = d
        #print (self.orderbook['bids'][0])
        

    def handle_orderBookL2(self, message):
        pass

    def __on_message(self, ws, message):
        '''Handler for parsing WS messages.'''


        self.msg_count +=1
        print (self.msg_count)

        message = json.loads(message)
        
        #self.logger.debug(json.dumps(message))

        table = message.get("table")
        action = message.get("action")

        #print ("message ", table)
        #print (message['data'])
        #print (action)
        #print (self.mid_price())
        #print (action, table, self.msg_count)
        try:

            if 'subscribe' in message:
                self.logger.debug("Subscribed to %s." % message['subscribe'])

            elif action:
                #print (table)

                if table == 'orderBook10':
                    
                    self.hanldle_book10(message)

                    #self.mid_price()

                """
                elif table == 'orderBookL2':
                    d = message['data']
                    #print ("...")
                    #if action != 'partial':
                    #    print (d)

                    #message['keys']

                if table not in self.data:
                    self.data[table] = []

                # There are four possible actions from the WS:
                # 'partial' - full table image
                # 'insert'  - new row
                # 'update'  - update row
                # 'delete'  - delete row
                if action == 'partial':
                    self.handle_paritial(table, message)
           
                elif action == 'insert':
                    self.handle_insert(table, message)

                elif action == 'update':
                    self.handle_update(table, message)

                elif action == 'delete':
                    self.handle_delete(table, message)
                """
                
                #else:
                #    raise Exception("Unknown action: %s" % action)
        except:
            self.logger.error(traceback.format_exc())

    def __on_error(self, ws, error):
        '''Called on fatal websocket errors. We exit on these.'''
        if not self.exited:
            self.logger.error("Error : %s" % error)
            raise websocket.WebSocketException(error)

    def __on_open(self):
        '''Called when the WS opens.'''
        self.logger.debug("Websocket Opened.")

    def __on_close(self):
        '''Called on websocket close.'''
        self.logger.info('Websocket Closed')


# Utility method for finding an item in the store.
# When an update comes through on the websocket, we need to figure out which item in the array it is
# in order to match that item.
#
# Helpfully, on a data push (or on an HTTP hit to /api/v1/schema), we have a "keys" array. These are the
# fields we can use to uniquely identify an item. Sometimes there is more than one, so we iterate through all
# provided keys.
def find_by_keys(keys, table, matchData):
    for item in table:
        if all(item[k] == matchData[k] for k in keys):
            return item

def order_leaves_quantity(o):
    if o['leavesQty'] is None:
        return True
    return o['leavesQty'] > 0