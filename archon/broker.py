"""
broker
"""

from archon.exchange.cryptopia import CryptopiaAPI
import archon.exchange.exchanges as exc
from archon.exchange.rex import Bittrex
from archon.markets import *
from archon.balances import *
from archon.exchange.kucoin import KuClient
import binance.client
import krakenex

import time
import pika
import sys
import time
import random
import json

#from util import *

clients = {}


class Broker:

    def __init__(self):
        self.s_exchange = None

    def set_mail_config(self, apikey, domain):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain

    def set_api_keys(self, exchange, key, secret):
        #print ("set api " + str(exchange))
        if exchange==exc.CRYPTOPIA:
            clients[exchange] = CryptopiaAPI(key, secret)
        elif exchange==exc.BITTREX:
            clients[exchange] = Bittrex(key,secret)  
        elif exchange==exc.KUCOIN:
            clients[exchange] = KuClient(key,secret)   
        elif exchange==exc.BINANCE:
            clients[exchange] = binance.client.Client(key,secret)
        elif exchange==exc.KRAKEN:        
            k = krakenex.API()
            k.load_key('kraken.key')
            clients[exchange] = k


    def get_client(self, EXC):
        """ directly get a client """
        return clients[EXC]

    def set_singleton_exchange(self, exchange):
        self.s_exchange = exchange       

    def balance_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange

        if exchange==exc.CRYPTOPIA:
            b, error = clients[exc.CRYPTOPIA].get_balance_all()        
            b = unify_balance(b,exchange)
            return b
        
        elif exchange==exc.BITTREX:
            b = clients[exc.BITTREX].get_balances()
            br = b["result"]
            br = unify_balance(br,exchange) 
            return br    

        elif exchange==exc.KUCOIN:
            b = clients[exc.KUCOIN].get_all_balances()       
            b = unify_balance(b,exchange) 
            return b        

        elif exchange==exc.BINANCE:
            b = clients[exc.BINANCE].get_account()['balances']
            b = unify_balance(b,exchange) 
            return b

        elif exchange==exc.KRAKEN:
            b = clients[exc.KRAKEN].query_private('Balance')
            r = b['result']
            r = unify_balance(r,exchange) 
            return r

    def balance_currency(self, currency, exchange=None):
        if exchange is None: exchange=self.s_exchange
        print ("balance_currency " + currency + " " + str(exchange))
        if exchange==exc.CRYPTOPIA:
            currency, err = clients[exc.CRYPTOPIA].get_balance(currency)        
            return currency['Total']
        elif exchange==exc.BITTREX:
            #{'Currency': 'BTC', 'Balance': 0.0, 'Available': 0.0, 'Pending': 0.0, 
            try:
                return_arg = clients[exc.BITTREX].get_balance(currency)        
                print (return_arg)
                result = return_arg['result']['Balance']
                return result
            except:
                return -1
        

    def get_total_balance(self, currency='USD',exchange=None):
        """Get total balance in your currency, USD by default"""
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            allb = self.balance_all(exchange)
            balance_list = list()
            for b in allb:
                if b['Total']>0:
                    d = {'symbol':b['Symbol'],'total':b['Total']}
                    balance_list.append(d)

            return balance_list

        elif exchange==exc.BITTREX:
            allb = self.balance_all(exchange)
            balance_list = list()
            for b in allb:
                #print (b)
                if b['Balance']>0:
                    d = {'symbol':b['Currency'],'total':b['Balance']}
                    balance_list.append(d)

            return balance_list

        elif exchange==exc.KUCOIN:
            # get balances
            balances = client.get_all_balances()
            # find unique coin names
            coins_csl = ','.join([b['coinType'] for b in balances])
            # get rates for these coins
            #currency_res = client.get_currencies(coins_csl)
            #rates = currency_res['rates']

            balance_list = list()
            for b in balances:
                # ignore any coins of 0 value
                if b['balanceStr'] == '0.0' and b['freezeBalanceStr'] == '0.0':
                    continue
                # ignore the coin if we don't have a rate for it
                #if b['coinType'] not in rates:
                #    continue

                d = {'symbol':b['coinType'],'total':b['balance']}
                balance_list.append(d)

            return balance_list
        

    def open_orders_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        # ("get open orders " + str(market))

        if exchange==exc.CRYPTOPIA:
            #oo, _ = clients[exc.CRYPTOPIA].get_openorders(market)                
            oo, _ = clients[exc.CRYPTOPIA].get_openorders_all()    
            return oo

        elif exchange==exc.BITTREX:
            #TODO
            #oo = api.get_open_orders(market)["result"]
            oo = clients[exc.BITTREX].get_open_orders()
            oor = oo["result"]
            return oor

    """
    def open_orders_market(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        # ("get open orders " + str(market))

        if exchange==exc.CRYPTOPIA:
            #oo, _ = clients[exc.CRYPTOPIA].get_openorders(market)                
            oo, _ = clients[exc.CRYPTOPIA].get_openorders_all()    
            return oo

        elif exchange==exc.BITTREX:
            #oo = api.get_open_orders(market)["result"]
            oo = clients[exc.BITTREX].get_open_orders()
            oor = oo["result"]
            return oor
    """

    def market_history(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_history(market)
            return txs

        elif exchange==exc.BITTREX:
            r = clients[exc.BITTREX].get_market_history(market)["result"]
            return r

    def trade_history(self, market, exchange=None):
        """ personal trades """
        if exchange is None: exchange=self.s_exchange
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_tradehistory(market)
            return txs

    def get_tradehistory_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_tradehistory_all()
            return txs

    def get_orderbook(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        #print ("get orderbook " + str(market))
        if exchange==exc.CRYPTOPIA:
            ob, err = clients[exc.CRYPTOPIA].get_orders(market)
            if err:
                print ("error " + str(err))
            else:
                #print (ob)
                bids = ob["Buy"]
                asks = ob["Sell"]    
                return [bids,asks]

        elif exchange==exc.BITTREX:            
            ob = clients[exc.BITTREX].get_orderbook(market)["result"]
            bids = (ob["buy"])
            asks = (ob["sell"])
            return [bids,asks]

    def submit_order(self, order, exchange=None):
        """ submit order which is array [type,order,qty] """
        # ("order " + str(order))         
        if exchange is None: exchange=self.s_exchange
        market,ttype,order_price,qty = order
        if exchange==exc.CRYPTOPIA:            
            # (order_price,qty,market)
            if ttype == "BUY":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "BUY", order_price, qty)
                if err:
                    print ("! error with order " + str(order) + " " + str(err))
                else:
                    print ("result " + str(result))
                    return result
            elif ttype == "SELL":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "SELL", order_price, qty)
                if err:
                    print ("error order " + str(order))
                else:
                    print ("result " + str(result))
        elif exchange==exc.BITTREX:
            #def trade_buy(self, market=None, order_type=None, quantity=None, rate=None, time_in_effect=None,
            #      condition_type=None, target=0.0):
            if ttype == "BUY":
                #def buy_limit(self, market, quantity, rate):
                result = clients[exc.BITTREX].buy_limit(market, qty, order_price)
                print (result)
            elif ttype == "SELL":
                clients[exc.BITTREX].trade_sell(market, "BUY", order_price, qty)


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
        if exchange==exc.CRYPTOPIA:
            print ("cancel CC " + str(oid))
            r,err = clients[exc.CRYPTOPIA].cancel_trade_id(oid)
            return r
        elif exchange==exc.BITTREX:
            r = clients[exc.BITTREX].cancel(oid)
            return r

    def cancel_all(self, market, exchange=None):
        #print ("cancel all.......")
        if exchange is None: exchange=self.s_exchange
        if exchange==exc.CRYPTOPIA:            
            print ("cancel all")
            oo, err = clients[exc.CRYPTOPIA].get_openorders(market)

            if err:
                return []
            else:
                print ("open orders ",oo)

                for o in oo:
                    self.cancel(o['OrderId'])
                #r, err = clients[exc.CRYPTOPIA].cancel_all_trades()
                #time.sleep(2)

                oo, _ = clients[exc.CRYPTOPIA].get_openorders(market)
                print ("open orders ",oo)

    """
    def get_market_summary(self, market):
        #if exchange is None: exchange=self.s_exchange
        #exchange = self.parse_exchange(**kwargs)
        client = clients[market.exchange]
        m = market.str_rep()
        if market.exchange==exc.CRYPTOPIA:
            result, err = client.get_market(m)
            return result
        elif market.exchange==exc.BITTREX:   
            print ("get " + m)
            r = client.get_market_summary(m)
            return r['result'][0]
    """

    def get_market_summary_str(self, market, exchange):        
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]        
        if exchange==exc.CRYPTOPIA:
            result, err = client.get_market(market)
            return result
        elif exchange==exc.BITTREX:   
            #print ("get " + market)
            r = client.get_market_summary(market)
            return r['result'][0]

    def get_market_summaries(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            r = client.get_markets()[0]
            f = lambda x: convert_markets_to(x, exchange)
            cc_markets = [f(x['Label']) for x in r]
            #TODO use object
            return cc_markets
        elif exchange==exc.BITTREX:   
            r = client.get_market_summaries()['result']
            f = lambda x: convert_markets_to(x, exchange)            
            rex_markets = [x['MarketName'] for x in r]
            rex_markets = [f(x) for x in rex_markets]
            #rex_markets = [Market(x,exc.BITTREX) for x in rex_markets]
            return rex_markets

    # ---- key names ----

    def price_key(self, **kwargs):
        if exchange is None: exchange=self.s_exchange        
        if exchange==exc.CRYPTOPIA:
            price_key = "Price"
            return price_key
        elif exchange==exc.BITTREX:
            price_key = "Rate"
            return price_key

    def qty_key(self, **kwargs):
        if exchange is None: exchange=self.s_exchange
        if exchange==exc.CRYPTOPIA:
            key = "Volume"
            return key
        elif exchange==exc.BITTREX:
            return "Quantity"

    def o_key_price(self, exchange):
        if exchange==exc.CRYPTOPIA:
            return "Rate"
        elif exchange==exc.BITTREX:
            return "Limit"

    def o_key_id(self, exchange):
        if exchange==exc.CRYPTOPIA:
            return "OrderId"
        elif exchange==exc.BITTREX:
            return "OrderUuid"
            
    def otype_key(self, exchange):
        if exchange==exc.CRYPTOPIA:
            return "Type"
        elif exchange==exc.BITTREX:
            return "OrderType"

    def otype_key_buy(self, exchange):
        if exchange==exc.CRYPTOPIA:
            return "Buy"
        elif exchange==exc.BITTREX:
            return "LIMIT_BUY"

    def otype_key_sell(self, exchange):
        if exchange==exc.CRYPTOPIA:
            return "Sell"
        elif exchange==exc.BITTREX:
            return "LIMIT_SELL"

    def tx_amount_key(self, **kwargs):
        if exchange==exc.CRYPTOPIA:
            return "Amount"

    def book_key_qty(self, exchange):
        if exchange==exc.CRYPTOPIA:
            key = "Volume"
            return key
        elif exchange==exc.BITTREX:
            return "Quantity"

    def book_key_price(self, exchange):
        if exchange==exc.CRYPTOPIA:
            key = "Price"
            return key
        elif exchange==exc.BITTREX:
            return "Rate"



    """
    def submit_order_type(self, order,  **kwargs):
        # submit order which is array [type,order,qty] 
        # ("order " + str(order)) 
        exchange = self.parse_exchange(**kwargs)
        if exchange==exc.CRYPTOPIA:
            market,ttype,order_price,qty = order.market, order.otype, order.price, order.qty
            # (order_price,qty,market)
            if ttype == "BUY":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "BUY", order_price, qty)
                if err:
                    print ("! error with order " + str(order) + " " + str(err))
                else:
                    print ("result " + str(result))
                    return result
            elif ttype == "SELL":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "SELL", order_price, qty)
                if err:
                    print ("error order " + str(order))
                else:
                    print ("result " + str(result))

        elif exchange==exc.BITTREX:
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
                r = clients[exc.BITTREX].buy_limit(market=market, quantity=Quantity, rate=Rate)
                #TODO handle fails
                print ("order result " + str(r))
            elif ttype == "SELL":
                r = clients[exc.BITTREX].sell_limit(market=market, quantity=Quantity, rate=Rate)
                print ("order result " + str(r))
    """
