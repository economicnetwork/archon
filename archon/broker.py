"""
broker
"""

from archon.cryptopia import CryptopiaAPI

#import bittrex
from archon.rex import Bittrex
#from . import markets
from archon.markets import *

import time
import pika
import sys
import time
import random
import json

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#channel = connection.channel()
#channel.exchange_declare(exchange='logs',
#                         exchange_type='fanout')

#from util import *


EXC_CRYPTOPIA = 0
EXC_BITTREX = 1
EXC_NAMES = {EXC_CRYPTOPIA:"Cryptopia",EXC_BITTREX:"Bittrex"}
BITTREX_NAME = "Bittrex"
CRYPTOPIA_NAME = "Cryptopia"
clients = {}

#clients = {
#    EXC_CRYPTOPIA:ccapi,
    #EXC_BITTREX:rexapi
#}


class Broker:

    def __init__(self):
        self.s_exchange = None

    def set_mail_config(self, apikey, domain):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain

    def set_api_keys(self, exchange, key, secret):
        if exchange==EXC_CRYPTOPIA:
            clients[exchange] = CryptopiaAPI(key, secret)
        elif exchange==EXC_BITTREX:
            clients[exchange] = Bittrex(key,secret)        

    def get_client(self, EXC):
        """ directly get a client """
        return clients[EXC]

    def set_singleton_exchange(self, exchange):
        self.s_exchange = exchange       

    def balance_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            currency_list, error = clients[EXC_CRYPTOPIA].get_balance_all()        
            return currency_list
        
        elif exchange==EXC_BITTREX:
            b = clients[EXC_BITTREX].get_balances()
            br = b["result"]
            return br            
        

    def balance_currency(self, currency, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            currency, err = clients[EXC_CRYPTOPIA].get_balance(currency)        
            return currency['Total']
        elif exchange==EXC_BITTREX:
            #{'Currency': 'BTC', 'Balance': 0.0, 'Available': 0.0, 'Pending': 0.0, 'CryptoAddress': '12bXpAZbb4uJ4VQ88QQvi6LwgAhaHURUNV'}
            return_arg = clients[EXC_BITTREX].get_balance(currency)        
            #print (return_arg)
            result = return_arg['result']['Balance']
            return result
            

    def open_orders_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        # ("get open orders " + str(market))

        if exchange==EXC_CRYPTOPIA:
            #oo, _ = clients[EXC_CRYPTOPIA].get_openorders(market)                
            oo, _ = clients[EXC_CRYPTOPIA].get_openorders_all()    
            return oo

        elif exchange==EXC_BITTREX:
            #TODO
            #oo = api.get_open_orders(market)["result"]
            oo = clients[EXC_BITTREX].get_open_orders()
            oor = oo["result"]
            return oor

    """
    def open_orders(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        # ("get open orders " + str(market))

        if exchange==EXC_CRYPTOPIA:
            #oo, _ = clients[EXC_CRYPTOPIA].get_openorders(market)                
            oo, _ = clients[EXC_CRYPTOPIA].get_openorders_all()    
            return oo

        elif exchange==EXC_BITTREX:
            #oo = api.get_open_orders(market)["result"]
            oo = clients[EXC_BITTREX].get_open_orders()
            oor = oo["result"]
            return oor
    """


    def market_history(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            txs, _ = clients[EXC_CRYPTOPIA].get_history(market)
            return txs

        elif exchange==EXC_BITTREX:
            r = clients[EXC_BITTREX].get_market_history(market)["result"]
            return r

    def trade_history(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            txs, _ = clients[EXC_CRYPTOPIA].get_tradehistory(market)
            return txs

    def get_tradehistory_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            txs, _ = clients[EXC_CRYPTOPIA].get_tradehistory_all()
            return txs

    def get_orderbook(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        #print ("get orderbook " + str(market))
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

    def submit_order(self, order, exchange=None):
        """ submit order which is array [type,order,qty] """
        # ("order " + str(order))         
        if exchange is None: exchange=self.s_exchange
        market,ttype,order_price,qty = order
        if exchange==EXC_CRYPTOPIA:            
            # (order_price,qty,market)
            if ttype == "BUY":
                result, err = clients[EXC_CRYPTOPIA].submit_trade(market, "BUY", order_price, qty)
                if err:
                    print ("! error with order " + str(order) + " " + str(err))
                else:
                    print ("result " + str(result))
                    return result
            elif ttype == "SELL":
                result, err = clients[EXC_CRYPTOPIA].submit_trade(market, "SELL", order_price, qty)
                if err:
                    print ("error order " + str(order))
                else:
                    print ("result " + str(result))
        elif exchange==EXC_BITTREX:
            #def trade_buy(self, market=None, order_type=None, quantity=None, rate=None, time_in_effect=None,
            #      condition_type=None, target=0.0):
            if ttype == "BUY":
                #def buy_limit(self, market, quantity, rate):
                result = clients[EXC_BITTREX].buy_limit(market, qty, order_price)
                print (result)
            elif ttype == "SELL":
                clients[EXC_BITTREX].trade_sell(market, "BUY", order_price, qty)


    """
    def submit_order_type(self, order,  **kwargs):
        # submit order which is array [type,order,qty] 
        # ("order " + str(order)) 
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            market,ttype,order_price,qty = order.market, order.otype, order.price, order.qty
            # (order_price,qty,market)
            if ttype == "BUY":
                result, err = clients[EXC_CRYPTOPIA].submit_trade(market, "BUY", order_price, qty)
                if err:
                    print ("! error with order " + str(order) + " " + str(err))
                else:
                    print ("result " + str(result))
                    return result
            elif ttype == "SELL":
                result, err = clients[EXC_CRYPTOPIA].submit_trade(market, "SELL", order_price, qty)
                if err:
                    print ("error order " + str(order))
                else:
                    print ("result " + str(result))

        elif exchange==EXC_BITTREX:
            #TODO
            market = "USDT-BTC"
            ttype,order_price,qty = order
            OrderType = "LIMIT"
            Quantity = qty
            Rate = order_price
            TimeInEffect = "GOOD_TIL_CANCELLED"
            ConditionType = "NONE"
            target = 0
            if ttype == "BUY":   
                #buy_limit(self, market, quantity, rate):         
                r = clients[EXC_BITTREX].buy_limit(market=market, quantity=Quantity, rate=Rate)
                #TODO handle fails
                print ("order result " + str(r))
            elif ttype == "SELL":
                r = clients[EXC_BITTREX].sell_limit(market=market, quantity=Quantity, rate=Rate)
                print ("order result " + str(r))
    """

    def submit_order_check(self, order):
        """ submit order but require user action """
        # ("order " + str(order))
        result = ask_user("submit order " + str(order)+ " ? ")
        if result:
            self.submit(order)
        else:
            # ("no")
            pass

    def cancel(self, oid, exchange=None):
        """ cancel by id . TODO integrate OMS and internal checks """
        if exchange is None: exchange=self.s_exchange
        print ("cancel " + str(oid) + " " + str(exchange))
        if exchange==EXC_CRYPTOPIA:
            print ("cancel CC " + str(oid))
            r,err = clients[EXC_CRYPTOPIA].cancel_trade_id(oid)
            return r
        elif exchange==EXC_BITTREX:
            r = clients[EXC_BITTREX].cancel(oid)
            return r


    def cancel_all(self, market, exchange=None):
        #print ("cancel all.......")
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:            
            print ("cancel all")
            oo, err = clients[EXC_CRYPTOPIA].get_openorders(market)

            if err:
                return []
            else:
                print ("open orders ",oo)

                for o in oo:
                    self.cancel(o['OrderId'])
                #r, err = clients[EXC_CRYPTOPIA].cancel_all_trades()
                #time.sleep(2)

                oo, _ = clients[EXC_CRYPTOPIA].get_openorders(market)
                print ("open orders ",oo)

    """
    def get_market_summary(self, market):
        #if exchange is None: exchange=self.s_exchange
        #exchange = self.parse_exchange(**kwargs)
        client = clients[market.exchange]
        m = market.str_rep()
        if market.exchange==EXC_CRYPTOPIA:
            result, err = client.get_market(m)
            return result
        elif market.exchange==EXC_BITTREX:   
            print ("get " + m)
            r = client.get_market_summary(m)
            return r['result'][0]
    """

    def get_market_summary_str(self, market, exchange):        
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]        
        if exchange==EXC_CRYPTOPIA:
            result, err = client.get_market(market)
            return result
        elif exchange==EXC_BITTREX:   
            #print ("get " + market)
            r = client.get_market_summary(market)
            return r['result'][0]

    def get_market_summaries(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==EXC_CRYPTOPIA:
            r = client.get_markets()[0]
            f = lambda x: convert_markets_to(x, exchange)
            cc_markets = [f(x['Label']) for x in r]
            #TODO use object
            return cc_markets
        elif exchange==EXC_BITTREX:   
            r = client.get_market_summaries()['result']
            f = lambda x: convert_markets_to(x, exchange)            
            rex_markets = [x['MarketName'] for x in r]
            rex_markets = [f(x) for x in rex_markets]
            #rex_markets = [Market(x,EXC_BITTREX) for x in rex_markets]
            return rex_markets


    def price_key(self, **kwargs):
        if exchange is None: exchange=self.s_exchange        
        if exchange==EXC_CRYPTOPIA:
            price_key = "Price"
            return price_key
        elif exchange==EXC_BITTREX:
            price_key = "Rate"
            return price_key

    def qty_key(self, **kwargs):
        if exchange is None: exchange=self.s_exchange
        if exchange==EXC_CRYPTOPIA:
            key = "Volume"
            return key
        elif exchange==EXC_BITTREX:
            return "Quantity"

    def tx_amount_key(self, **kwargs):
        if exchange==EXC_CRYPTOPIA:
            key = "Amount"
            return key

    # ---- experimental MQ -----
    def pub(self, tx):
        del tx['_id']
        jmsg = json.dumps(tx)
        #msg = json.dumps(data)
        channel.basic_publish(exchange='logs',
                        routing_key='',
                        body=jmsg)
        print("pub new tx %r" % jmsg)


    #def pub_thread(self):