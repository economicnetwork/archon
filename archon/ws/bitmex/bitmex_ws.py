import websocket
import threading
import traceback
from time import sleep
import json
import urllib
import math
from archon.ws.api_util import generate_nonce, generate_signature
from archon.ws.bitmex.bitmex_topics import *
#from loguru import logger
import pdb
import logging
import colorlog
import sys

table_orderbook = 'orderBook10'
table_instrument = 'instrument'

import logging

endpoint_V1 = "https://www.bitmex.com/api/v1"

        
# implementation of connecting to BitMEX websocket for streaming realtime data.
# On connect, it synchronously asks for a push of all this data then returns.

class BitMEXWebsocket:

    # Don't grow a table larger than this amount. Helps cap memory usage.
    MAX_TABLE_LEN = 200

    def __init__(self, symbol, api_key=None, api_secret=None, endpoint=endpoint_V1):
        '''Connect to the websocket and initialize data stores.'''        

        logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format("./log", "bitmex")),
            logging.StreamHandler(sys.stdout),
            #ColoredLogger
            #colorlog.StreamHandler(sys.stdout)
        ])
        self.logger = logging.getLogger()

        handler = colorlog.StreamHandler()
        #handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(name)s:%(message)s'))
        handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(message)s'))
        logger = colorlog.getLogger('colorexample')
        logger.addHandler(handler)

        #logging.setLoggerClass(ColoredLogger)
        self.logger.debug("bitmex - initializing WebSocket.")

        self.endpoint = endpoint
        self.symbol = symbol

        self.msg_processed = 0

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')
        
        self.api_key = api_key
        self.api_secret = api_secret

        self.data = {}
        self.keys = {}
        self.exited = False

        #assume one symbol for now
        self.orderbook = {}

        #define topics to subscribe to

        """
        Orderbook topics
        
        orderBook10 pushes the top 10 levels on every tick, but transmits much more data. 
        orderBookL2 pushes the full L2 order book, but the payload can get very large.
        In the future, orderBook10 may be throttled, so use orderBookL2_25 in any latency-sensitive application. 
        For those curious, the id on an orderBookL2_25 or orderBookL2 entry is a composite of price and symbol, 
        and is always unique for any given price level. It should be used to apply update and delete actions.
        
        "orderBook10",         // Top 10 levels using traditional full book push
        "orderBookL2_25",      // Top 25 levels of level 2 order book
        "orderBookL2",         // Full level 2 order book                

        sub to orderBookL2 for all levels, or orderBook10 for top 10 levels & save bandwidth
        """

        #self.symbolSubs = [TOPIC_execution, TOPIC_instrument, TOPIC_order, TOPIC_orderBook10, TOPIC_position, TOPIC_quote, TOPIC_trade]
        #account_sub_topics = {TOPIC_margin, TOPIC_position, TOPIC_order, TOPIC_orderBook10}
        #symbol_topics = {TOPIC_instrument, TOPIC_trade, TOPIC_quote}

        #data loop
        #1 subscribe 
        #2 wait for subscription success
        #3 handle update (could e.g. ignore updates)        

        #self.symbolSubs = [TOPIC_orderBookL2_25]
        self.symbolSubs = [TOPIC_instrument, TOPIC_orderBook10, TOPIC_quote, TOPIC_trade]
        self.genericSubs = [TOPIC_margin]

        symbol_subscriptions = [sub + ':' + self.symbol for sub in self.symbolSubs]
        self.subscriptions = symbol_subscriptions  + self.genericSubs

        self.logger.info("subscriptions %s"%str(self.subscriptions))

        self.all_topics = self.symbolSubs + self.genericSubs
        self.subscribed = list()

        # We can subscribe right in the connection querystring, so let's build that.
        # Subscribe to all pertinent endpoints
        wsURL = self.__get_url()
        self.logger.info("Connecting to %s" % wsURL)
        self.__connect(wsURL, symbol)
        self.logger.info('Connected to WS.')

        # Connected. Wait for partials

        #self.subscribe_topic(TOPIC_orderBook10)
        
        self.logger.info('Wait for initial data')

        self.got_init_data = False
        
        #TODO
        #self.__wait_for_subscription()

        #self.__wait_for_symbol(symbol)
        #if api_key:
        #self.__wait_for_account()

        self.got_init_data = True
        
        self.logger.info('Got all market data. Starting.')

    def exit(self):
        '''Call this to exit - will close websocket.'''
        self.exited = True
        self.ws.close()


    def subscribe_topic(self, topic):
        #{"op": "subscribe", "args": ["orderBookL2_25:XBTUSD"]}
        symbol = "XBTUSD"
        #args = ["orderBookL2_25:" + symbol]
        args = [topic + ":" + symbol]
        self.__send_command("subscribe",args)

    def get_instrument(self):
        '''Get the raw instrument data for this symbol.'''
        # Turn the 'tickSize' into 'tickLog' for use in rounding
        print ("?? ",instrument)
        instrument = self.data['instrument'][0]
        #instrument['tickLog'] = int(math.fabs(math.log10(instrument['tickSize'])))
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
        #TODO fix
        #instrument = self.data['instrument'][0]
        #d = {k: round(float(v or 0), instrument['tickLog']) for k, v in ticker.items()}
        return ticker

    def funds(self):
        '''Get your margin details.'''
        return self.data['margin'][0]

    def market_depth(self):
        '''Get market depth (orderbook). Returns all levels.'''
        #return self.data['orderBookL2']
        #return self.data['orderBook10']
        return self.orderbook

    def open_orders(self, clOrdIDPrefix):
        '''Get all your open orders.'''
        orders = self.data['order']
        # Filter to only open orders (leavesQty > 0) and those that we actually placed
        return [o for o in orders if str(o['clOrdID']).startswith(clOrdIDPrefix) and o['leavesQty'] > 0]

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

        self.logger.debug("exit connect")

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
                
        self.logger.info("subscribe to %s"%(str(self.subscriptions)))

        urlParts = list(urllib.parse.urlparse(self.endpoint))
        urlParts[0] = urlParts[0].replace('http', 'ws')
        urlParts[2] = "/realtime?subscribe={}".format(','.join(self.subscriptions))
        return urllib.parse.urlunparse(urlParts)

    def missing_topics(self):
        
        k = self.data.keys()
        self.logger.debug(k)
        delta = self.all_topics - k
        if len(delta) > 0:
            self.logger.error("missing %s"%delta)

            for missing_topic in delta:
                self.logger.debug("subscribe again missing topic %s"%missing_topic)
                self.subscribe_topic(missing_topic)

    def __wait_for_account(self):
        '''account topics. On subscribe, this data will come down. Wait for it.'''
        # Wait for the keys to show up from the ws
        #TODO ensure this is what we subscribe to
        self.logger.debug(self.data)
        account_sub_topics = {TOPIC_margin, TOPIC_position, TOPIC_order, TOPIC_orderBook10}
        while not account_sub_topics <= set(self.data):
            self.logger.debug("__wait_for_account")
            self.missing_topics()
            """
            k = self.data.keys()
            self.logger.debug(k)
            delta = account_sub_topics - k
            self.logger.debug("missing %s"%delta)
            """
            sleep(1.0)

    def __wait_for_symbol(self, symbol):
        '''symobl topics. On subscribe, this data will come down. Wait for it.'''
        symbol_topics = {TOPIC_instrument, TOPIC_trade, TOPIC_quote}
        while not symbol_topics <= set(self.data):
            self.logger.debug("__wait_for_symbols ")
            self.missing_topics()
            """
            k = self.data.keys()
            self.logger.debug(k)
            delta = symbol_topics - k
            self.logger.debug("missing %s"%delta)
            """
            sleep(1.0)

    def __wait_for_subscription(self):
        sub_all = False
        while not sub_all:
            print ("subscribed " ,self.subscribed)
            time.sleep(1.0)
            #self.subscribed

    def __send_command(self, command, args=None):
        '''Send a raw command.'''
        if args is None:
            args = []
        self.ws.send(json.dumps({"op": command, "args": args}))

    def handle_partial(self, table, message):
        self.logger.debug("%s: partial" % table)
        self.data[table] += message['data']
        self.logger.debug("keys now %s" % self.data.keys())
        # Keys are communicated on partials to let you know how to uniquely identify
        # an item. We use it for updates.
        self.keys[table] = message['keys']

    def handle_insert(self, table, message):
        self.logger.debug('%s: inserting %s' % (table, message['data']))
        self.data[table] += message['data']

        # Limit the max length of the table to avoid excessive memory usage.
        # Don't trim orders because we'll lose valuable state if we do.
        if table not in ['order', 'orderBookL2'] and len(self.data[table]) > BitMEXWebsocket.MAX_TABLE_LEN:
            self.data[table] = self.data[table][int(BitMEXWebsocket.MAX_TABLE_LEN / 2):]

    #def handle_update_book_incremental(self):
    #    #orderBookL2_25

    def handle_update_bookpush(self, message):        
        """orderBook10"""
        self.logger.debug("book push %s"%message)
        #!! assumes only 1 update
        data = message['data'][0]
        bids = data['bids']
        asks = data['asks']
        self.orderbook["bids"] = bids
        self.orderbook["asks"] = asks



    def handle_update(self, table, message):
        #self.logger.debug('%s: updating %s' % (table, message['data']))
        # Locate the item in the collection and update it.
        self.logger.debug("update %s %s"%(table,self.keys))
        data = message['data']
        if table == TOPIC_orderBook10:
            self.handle_update_bookpush(message)

        else:
            for updateData in data:
                self.logger.debug("udpate item %s"%updateData)
                item = findItemByKeys(self.keys[table], self.data[table], updateData)
                if not item:
                    return  # No item found to update. Could happen before push
                item.update(updateData)
                # Remove cancelled / filled orders
                if table == 'order' and item['leavesQty'] <= 0:
                    self.data[table].remove(item)

    def handle_delete(self, table, message):
        self.logger.debug('%s: deleting %s' % (table, message['data']))
        # Locate the item in the collection and remove it.
        for deleteData in message['data']:
            item = findItemByKeys(self.keys[table], self.data[table], deleteData)
            self.data[table].remove(item)

    def __on_message(self, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        
        msg = json.dumps(message)
        self.logger.debug(msg)
        #pdb.set_trace()
        #self.logger.debug("got msg. %s %s"%str(self.got_init_data),set(self.data))
        #self.missing_topics()
        self.logger.debug("keys %s"%str(self.data.keys()))

        table = message['table'] if 'table' in message else None
        action = message['action'] if 'action' in message else None

        #logdebug = True
            
        try:
            if 'subscribe' in message:
                topic = message['subscribe']
                self.logger.info("Subscribed to %s." % topic)
                self.logger.info(msg)
                self.subscribed.append(topic)
                self.data[topic] = []


            elif action:
                #print (action," ",table)
                #Handle first update
                
                if table not in self.data:
                    #new table
                    self.logger.info("!! new data %s"%table)
                    self.data[table] = []

                #TODO should check what is the status

                # four possible actions
                # 'partial' - full table image
                # 'insert'  - new row
                # 'update'  - update row
                # 'delete'  - delete row
                if action == 'partial':
                    self.handle_partial(table, message)                    

                elif action == 'insert':
                    self.handle_insert(table, message)                    

                elif action == 'update':
                    self.handle_update(table, message)

                elif action == 'delete':
                    self.handle_delete(table, message)
                    
                else:
                    raise Exception("Unknown action: %s" % action)
        except:
            e = traceback.format_exc()     
            self.logger.error("error on msg %s"%msg)       
            self.logger.error("! %s"%e)

        self.msg_processed +=1
        if self.msg_processed%10==0:
            self.logger.debug("self.msg_processed %i "%self.msg_processed)

        

    def __on_error(self, error):
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
def findItemByKeys(keys, table, matchData):
    for item in table:
        matched = True
        for key in keys:
            if item[key] != matchData[key]:
                matched = False
        if matched:
            return item
