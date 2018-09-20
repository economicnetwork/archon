"""
broker
"""

from archon.cryptopia import CryptopiaAPI#import rex
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

    def set_mail_config(self, apikey, domain):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain

    def set_api_keys(self, exchange, key, secret):
        clients[exchange] = CryptopiaAPI(key, secret)
        #rexapi = rex.Bittrex(rex_key,rex_secret)
        #return ccapi

    def get_client(self, EXC):
        """ directly get a client """
        return clients[EXC]

    def set_singleton_exchange(self, exchange):
        self.s_exchange = exchange

    def parse_exchange(self, **kwargs):
        """ parse keywords and check set singleton """
        if self.s_exchange != None:
            return self.s_exchange
        else:
            return kwargs['exchange']        

    def balance_all(self, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            currency_list, error = clients[EXC_CRYPTOPIA].get_balance_all()        
            return currency_list

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
        print ("get orderbook " + str(market))
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

    def submit_order(self, order,  **kwargs):
        """ submit order which is array [type,order,qty] """
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

    def cancel(self, oid, **kwargs):
        """ cancel by id . TODO integrate OMS and internal checks """
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            print ("cancel " + str(oid))
            r,err = clients[EXC_CRYPTOPIA].cancel_trade_id(oid)
            return r
        elif exchange==EXC_BITTREX:
            r = clients[EXC_BITTREX].cancel(oid)
            return r


    def cancel_all(self, market, **kwargs):
        #print ("cancel all.......")
        exchange = self.parse_exchange(**kwargs)
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


    def price_key(self, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            price_key = "Price"
            return price_key
        elif exchange==EXC_BITTREX:
            price_key = "Rate"
            return price_key

    def qty_key(self, **kwargs):
        exchange = self.parse_exchange(**kwargs)
        if exchange==EXC_CRYPTOPIA:
            key = "Volume"
            return key
        elif exchange==EXC_BITTREX:
            return "Quantity"

    def tx_amount_key(self, **kwargs):
        if exchange==EXC_CRYPTOPIA:
            key = "Amount"
            return key
        
    #single_client = None
    #market = "AC3_BTC"
