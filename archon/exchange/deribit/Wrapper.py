"""
deribit wrapper

fees
Perpetual Contracts
Maker Rebate: 0.025%
Taker Fee: 0.075%

Futures
Maker Rebate: 0.02%
Taker Fee: 0.05%
"""

import time, hashlib, base64, sys
from collections import OrderedDict
from archon.exchange.deribit.ws.deribit_ws import DeribitWebsocket
import logging

import requests
from archon.custom_logger import setup_logger

instrument_btc_perp = "BTC-PERPETUAL"
instrument_btc_june ="BTC-28JUN19"
instrument_btc_march = "BTC-29MAR19"


base_public_api = "/api/v1/public/"
base_private_api = "/api/v1/private/"


class DeribitWrapper(object):

    def __init__(self, key=None, secret=None, url=None):
        setup_logger(logger_name="DeribitWrapper", log_file='DeribitWrapper.log')
        self.logger = logging.getLogger("DeribitWrapper")
        self.key = key
        self.secret = secret
        self.session = requests.Session()
        self.ws = DeribitWebsocket()
        self.ws.connect()
        
        if url:
            self.url = url
        else:
            self.url = "https://www.deribit.com"

        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)            

    def _deri_request(self, action, data):
        try:
            response = None        
            if action.startswith("/api/v1/private/"):
                if self.key is None or self.secret is None:
                    raise Exception("Key or secret empty")

                signature = self.generate_signature(action, data)
                
                response = self.session.post(self.url + action, data=data, headers={'x-deribit-sig': signature},
                                            verify=True)
            else:
                response = self.session.get(self.url + action, params=data, verify=True)

            if response.status_code != 200:
                raise Exception("Wrong response code: {0}".format(response.status_code))

            json = response.json()

            if json["success"] == False:
                raise Exception("Failed: " + json["message"])

            if "result" in json:
                return json["result"]
            elif "message" in json:
                return json["message"]
            else:
                return "Ok"
        except Exception as err:
            self.logger.error(err)

    def generate_signature(self, action, data):
        tstamp = int(time.time() * 1000)
        signature_data = {
            '_': tstamp,
            '_ackey': self.key,
            '_acsec': self.secret,
            '_action': action
        }
        signature_data.update(data)
        sorted_signature_data = OrderedDict(sorted(signature_data.items(), key=lambda t: t[0]))

        def converter(data):
            key = data[0]
            value = data[1]
            if isinstance(value, list):
                return '='.join([str(key), ''.join(value)])
            else:
                return '='.join([str(key), str(value)])

        items = map(converter, sorted_signature_data.items())

        signature_string = '&'.join(items)

        sha256 = hashlib.sha256()
        sha256.update(signature_string.encode("utf-8"))
        sig = self.key + "." + str(tstamp) + "."
        sig += base64.b64encode(sha256.digest()).decode("utf-8")
        return sig

    def getorderbook(self, instrument):
        return self._deri_request(base_public_api + "getorderbook", {'instrument': instrument})

    def json_depth(self, instrument):
        return self.ws.market_depth(instrument)

    def voi(self,n,instrument):
        bids_volume = self.ws.market_depth(instrument)['bids'][n]['cm']
        asks_volume = self.ws.market_depth(instrument)['asks'][n]['cm']
        return round((bids_volume - asks_volume) / (bids_volume + asks_volume), 2)

    def bids(self,instrument):
        bids = [[row['price'], row['quantity']] for row in self.ws.market_depth(instrument)['bids']]
        return bids

    def closest_bid(self, instrument):
        return self.ws.market_depth(instrument)['bids'][0]

    def closest_ask(self, instrument):
        return self.ws.market_depth(instrument)['asks'][0]

    def asks(self,instrument):
        asks = [[row['price'], row['quantity']] for row in self.ws.market_depth(instrument)['asks']]
        return asks

    def spread(self, instrument1, instrument2):
        inst1_bid = self.ws.market_depth(instrument1)['bids'][0]['price']
        inst1_ask = self.ws.market_depth(instrument1)['asks'][0]['price']
        inst2_bid = self.ws.market_depth(instrument2)['bids'][0]['price']
        inst2_ask = self.ws.market_depth(instrument2)['asks'][0]['price']
        spread = (inst2_bid -  inst1_bid) / inst1_bid
        return spread

    def get_last_trade(self,instrument):
        return self.ws.market_depth(instrument)['last']

    def getinstruments(self):
        return self._deri_request(base_public_api + "getinstruments", {})

    def getcurrencies(self):
        return self._deri_request(base_public_api + "getcurrencies", {})

    def getlasttrades(self, instrument, count=None, since=None):
        options = {
            'instrument': instrument
        }

        if since:
            options['since'] = since

        if count:
            options['count'] = count

        return self._deri_request(base_public_api + "getlasttrades", options)

    def getsummary(self, instrument):
        return self._deri_request(base_public_api + "getsummary", {"instrument": instrument})

    def index(self):
        return self._deri_request(base_public_api + "index", {})

    def stats(self):
        return self._deri_request(base_public_api + "stats", {})

    def account(self):
        return self._deri_request("/api/v1/private/account", {})

    def buy(self, instrument, quantity, price, postOnly=None, label=None):
        options = {
            "instrument": instrument,
            "quantity": quantity,
            "price": price
        }

        if label:
            options["label"] = label

        if postOnly:
            options["postOnly"] = postOnly

        return self._deri_request("/api/v1/private/buy", options)

    def sell(self, instrument, quantity, price, postOnly=None, label=None):
        options = {
            "instrument": instrument,
            "quantity": quantity,
            "price": price
        }

        if label:
            options["label"] = label
        if postOnly:
            options["postOnly"] = postOnly

        return self._deri_request("/api/v1/private/sell", options)

    def cancel(self, orderId):
        options = {
            "orderId": orderId
        }

        return self._deri_request("/api/v1/private/cancel", options)

    def cancelall(self, typeDef="all"):
        return self._deri_request("/api/v1/private/cancelall", {"type": typeDef})

    def edit(self, orderId, quantity, price):
        options = {
            "orderId": orderId,
            "quantity": quantity,
            "price": price
        }

        return self._deri_request("/api/v1/private/edit", options)

    def getopenorders(self, instrument=None, orderId=None):
        options = {}

        if instrument:
            options["instrument"] = instrument
        if orderId:
            options["orderId"] = orderId

        return self._deri_request("/api/v1/private/getopenorders", options)

    def positions(self):
        return self._deri_request("/api/v1/private/positions", {})

    def orderhistory(self, count=None):
        options = {}
        if count:
            options["count"] = count

        return self._deri_request("/api/v1/private/orderhistory", options)

    def tradehistory(self, countNum=None, instrument="all", startTradeId=None):
        options = {
            "instrument": instrument
        }

        if countNum:
            options["count"] = countNum
        if startTradeId:
            options["startTradeId"] = startTradeId

        return self._deri_request("/api/v1/private/tradehistory", options)