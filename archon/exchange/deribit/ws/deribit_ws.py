from deribit_api import RestClient
import websocket
import json
import ssl
import threading
import logging
from archon.custom_logger import setup_logger

def on_open(ws):
    """
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())
    """
    print ("open")
    print (ws.sock.connected)


class DeribitWebsocket():

    def __init__(self):
        self.client = RestClient('', '')
        self.table = {}
        #self.logger = logging.getLogger('root')
        self.__reset()

        setup_logger(__name__, 'DeribitWebsocket.log')
        self.logger = logging.getLogger(__name__)        

        # disable all loggers from different files
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
        logging.getLogger('websockets.server').setLevel(logging.ERROR)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)
        logging.getLogger('websocket-client').setLevel(logging.ERROR)

        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)

    def on_message(self, ws, message):
        print ("message ",message)
        message = json.loads(message)
        if 'notifications' in message:
            self.table[message['notifications'][0]['result']['instrument']] = message['notifications'][0]['result']

    def on_error(self, ws, error):
        self.logger.error("error %s"%str(error))
        print (str(error))

    def on_close(self, ws):
        self.logger.info("### closed ###")

    def market_depth(self, symbol):
        return self.table[symbol]

    def on_open(self, ws):
        self.logger.info("ws on_open")   
        self.logger.info("connected %s" %str(ws.sock.connected))
        
        data = {
            "id": 5533,
            "action": "/api/v1/private/subscribe",
            "arguments": {
                #"instrument": ["all"],
                #"instrument": ["BTC-29DEC17"],
                "instrument": ["BTC-PERPETUAL"],
                "event": ["order_book"]
            }
        }

        data['sig'] = self.client.generate_signature(data['action'], data['arguments'])
        self.logger.info("subscribe")
        print (data)

        ws.send(json.dumps(data))
        #print (dir(ws))
        #print (ws.sock.connected)
        

    def connect(self):
        self.logger.info("connect ws")
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://www.deribit.com/ws/api/v1/",
                                  on_message = lambda ws,msg: self.on_message(ws, msg),
                                  on_error   = lambda ws,msg: self.on_error(ws, msg),
                                  on_open    = lambda ws:  self.on_open(ws),
                                  #on_open = self.on_open,                                  
                                  on_close = self.on_close)
        ssl_defaults = ssl.get_default_verify_paths()
        sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(sslopt=sslopt_ca_certs))
        self.wst.daemon = True
        self.wst.start()
        self.logger.info("Started thread")
        #TOOD subscribe later
        #self.ws.run_forever()

    def __reset(self):
        self.data = {}
        self.keys = {}
        self.exited = False
        self._error = None


