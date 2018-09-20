"""
broker
"""

from cryptopia import CryptopiaAPI
#import rex
import time
#from util import *


EXC_CRYPTOPIA = 0
EXC_BITTREX = 1

clients = {}

#clients = {
#    EXC_CRYPTOPIA:ccapi,
    #EXC_BITTREX:rexapi
#}


class Broker:

    def __init__(self):
        self.s_exchange = None

    def set_api_keys(self, exchange, key, secret):
        clients[exchange] = CryptopiaAPI(key, secret)
        #rexapi = rex.Bittrex(rex_key,rex_secret)
        #return ccapi

    def set_singleton_exchange(self, exchange):
        self.s_exchange = exchange

    def parse_exchange(self, **kwargs):
        """ parse keywords and check set singleton """
        if self.s_exchange != None:
            return self.s_exchange
        else:
            return kwargs['exchange']        

    def balance_currency(self, currency, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            currency, err = clients[EXC_CRYPTOPIA].get_balance(currency)        
            return currency

    def open_orders(self, market, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        # ("get open orders " + str(market))

        if exchange==EXC_CRYPTOPIA:
            oo, _ = clients[EXC_CRYPTOPIA].get_openorders(market)    
            return oo

        elif exchange==EXC_BITTREX:
            #oo = api.get_open_orders(market)["result"]
            oo = clients[EXC_BITTREX].get_open_orders(market)
            oor = oo["result"]
            return oor

    def market_history(self, market, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            txs, _ = clients[EXC_CRYPTOPIA].get_history(market)
            return txs

        elif exchange==EXC_BITTREX:
            r = clients[EXC_BITTREX].get_market_history(market)["result"]
            return r

    def trade_history(self, market, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            txs, _ = clients[EXC_CRYPTOPIA].get_tradehistory(market)
            return txs

    def get_orderbook(self, market, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            ob, err = clients[EXC_CRYPTOPIA].get_orders(market)
            if err:
                print ("error " + str(err))
            else:
                #print (ob)
                bids = ob["Buy"]
                asks = ob["Sell"]    
                return [bids,asks]

        elif exchange==EXC_BITTREX:
            
            ob = clients[EXC_BITTREX].get_orderbook(market)["result"]
            bids = (ob["buy"])
            asks = (ob["sell"])
            return [bids,asks]

    #single_client = None
    #market = "AC3_BTC"
