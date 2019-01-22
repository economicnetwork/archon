from deribit_api import RestClient
import websocket
import json
import ssl
import threading
import logging
from archon.custom_logger import setup_logger

class DeribitWebsocket():
    def __init__(self):
        self.client = RestClient('', '')
        self.table = {}
        #self.logger = logging.getLogger('root')
        self.__reset()

        setup_logger(__name__, 'strategy.log')
        self.logger = logging.getLogger(__name__)        

        # disable all loggers from different files
        logging.getLogger('asyncio').setLevel(logging.ERROR)
        logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
        logging.getLogger('websockets.server').setLevel(logging.ERROR)
        logging.getLogger('websockets.protocol').setLevel(logging.ERROR)

    def on_message(self, ws, message):
        message = json.loads(message)
        if 'notifications' in message:
            self.table[message['notifications'][0]['result']['instrument']] = message['notifications'][0]['result']

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def market_depth(self, symbol):
        return self.table[symbol]

    def on_open(self, ws):
        data = {
            "id": 5533,
            "action": "/api/v1/private/subscribe",
            "arguments": {
                "instrument": ["all"],
                "event": ["order_book"]
            }
        }
        data['sig'] = self.client.generate_signature(data['action'], data['arguments'])

        ws.send(json.dumps(data))

    def connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://www.deribit.com/ws/api/v1/",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        ssl_defaults = ssl.get_default_verify_paths()
        sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(sslopt=sslopt_ca_certs))
        self.wst.daemon = True
        self.wst.start()
        self.logger.info("Started thread")
        self.ws.on_open = self.on_open
        #self.ws.run_forever()

    def __reset(self):
        self.data = {}
        self.keys = {}
        self.exited = False
        self._error = None


