"""
broker

unified interface to exchanges
"""

import archon.exchange.exchanges as exc
from archon.util import *

from archon.model import models

#Wrappers
from archon.exchange.rex import Bittrex
from archon.exchange.cryptopia import CryptopiaAPI
from archon.exchange.kucoin import KuClient
import archon.exchange.hitbtc as hitbtc
from pymongo import MongoClient

#Wrappers with foreign package
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

logpath = './log'
log = setup_logger(logpath, 'broker_logger', 'broker')


class Broker:

    def __init__(self):
        log.info("init broker")
        self.s_exchange = None
        self.active_exchanges = list()

    def set_api_keys(self, exchange, key, secret):
        """ set clients, assumes conf file present """
        log.debug("set api " + str(exchange))
        if exchange==exc.CRYPTOPIA:
            clients[exchange] = CryptopiaAPI(key, secret)
        elif exchange==exc.BITTREX:
            clients[exchange] = Bittrex(key,secret)  
        elif exchange==exc.KUCOIN:
            clients[exchange] = KuClient(key,secret)   
        elif exchange==exc.HITBTC:
            clients[exchange] = hitbtc.RestClient(key,secret)   
        elif exchange==exc.BINANCE:
            clients[exchange] = binance.client.Client(key,secret)
        elif exchange==exc.KRAKEN:        
            clients[exchange] = krakenex.API(key,secret)

    def set_mail_config(self, apikey, domain, email_from, email_to):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain
        self.email_from = email_from
        self.email_to = email_to

    def set_mongo(self, url, dbName):
        #self.mongoHost = mongoHost
        #self.mongoPort = mongoPort
        self.mongo_url = url
        log.info("using mongo " + str(url))
        self.mongoclient = MongoClient(self.mongo_url)
        self.db = self.mongoclient[dbName]

    def get_db(self):
        return self.db

    def get_client(self, EXC):
        """ directly get a client """
        return clients[EXC]

    def set_singleton_exchange(self, exchange):
        self.s_exchange = exchange  


    # --- trading info ---

    def balance_all(self, exchange=None):
        log.info("balance")
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            b, error = clients[exc.CRYPTOPIA].get_balance_all()        
            b = models.conv_balance(b,exchange)
            return b
        
        elif exchange==exc.BITTREX:
            b = clients[exc.BITTREX].get_balances()
            br = b["result"]
            br = models.conv_balance(br,exchange) 
            return br    

        elif exchange==exc.KUCOIN:
            b = clients[exc.KUCOIN].get_all_balances()       
            b = models.conv_balance(b,exchange) 
            return b        

        elif exchange==exc.BINANCE:
            b = clients[exc.BINANCE].get_account()['balances']
            b = models.conv_balance(b,exchange) 
            return b

        elif exchange==exc.HITBTC:      
            b = client.get_trading_balance()        
            b = models.conv_balance(b,exchange)
            return b

        elif exchange==exc.KRAKEN:
            b = clients[exc.KRAKEN].query_private('Balance')
            r = b['result']
            r = models.conv_balance(r,exchange) 
            return r            

    def balance_currency(self, currency, exchange=None):
        if exchange is None: exchange=self.s_exchange
        log.info("balance_currency " + currency + " " + str(exchange))
        if exchange==exc.CRYPTOPIA:
            currency, err = clients[exc.CRYPTOPIA].get_balance(currency)        
            return currency['Total']
        elif exchange==exc.BITTREX:
            #{'Currency': 'BTC', 'Balance': 0.0, 'Available': 0.0, 'Pending': 0.0, 
            try:
                return_arg = clients[exc.BITTREX].get_balance(currency)        
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
                if b['Balance']>0:
                    d = {'symbol':b['Currency'],'total':b['Balance']}
                    balance_list.append(d)

            return balance_list

        elif exchange==exc.KUCOIN:
            balances = client.get_all_balances()

            balance_list = list()
            for b in balances:
                # ignore any coins of 0 value
                if b['balanceStr'] == '0.0' and b['freezeBalanceStr'] == '0.0':
                    continue

                d = {'symbol':b['coinType'],'total':b['balance']}
                balance_list.append(d)

            return balance_list        

    def trade_history(self, market, exchange=None):
        """ personal trades """
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_tradehistory(market)
            return txs
        elif exchange==exc.BITTREX:
            pass
        elif exchange==exc.KUCOIN:
            r = client.get_dealt_orders(limit=100)
            f = lambda x: models.conv_usertx(x,exchange)
            r = list(map(f,r))
            return r
            
    def get_tradehistory_all(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            txs, _ = client.get_tradehistory_all()
            return txs
        elif exchange==exc.BITTREX:
            r = client.get_order_history()
            return r
        elif exchange==exc.KUCOIN:
            r = client.get_dealt_orders(limit=100)['datas']
            f = lambda x: models.conv_usertx(x,exchange)
            tx = list(map(f,r))
            return tx

    def open_orders_symbol(self, symbol, exchange=None):
        if exchange is None: exchange=self.s_exchange
        oo = None
        if exchange==exc.CRYPTOPIA:
            oo, _ = clients[exc.CRYPTOPIA].get_openorders_all()    

        elif exchange==exc.BITTREX:
            oo = clients[exc.BITTREX].get_open_orders()["result"]
            f = lambda x: models.conv_openorder(x,exchange)
            oo = list(map(f,oo))  

        elif exchange==exc.KUCOIN:
            oo = clients[exc.KUCOIN].get_active_orders(symbol, kv_format=True)
            if len(oo) > 0:
                b = oo['BUY']
                a = oo['SELL']
                l = list()
                for x in b: l.append(models.conv_openorder(x,exchange))
                for x in a: l.append(models.conv_openorder(x,exchange))
                oo = l
            else:
                oo = []
        n = exc.NAMES[exchange]
        #log.info("open orders: " + str(n) + " " + str(oo))
        return oo

    def open_orders(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        #log.info("get open orders " + str(exchange))

        oo = None
        if exchange==exc.CRYPTOPIA:
            oo, _ = clients[exc.CRYPTOPIA].get_openorders_all()    
            f = lambda x: models.conv_openorder(x,exchange)
            oo = list(map(f,oo))  

        elif exchange==exc.BITTREX:
            #TODO
            #oo = api.get_open_orders(market)["result"]
            oo = clients[exc.BITTREX].get_open_orders()["result"]            
            f = lambda x: models.conv_openorder(x,exchange)
            oo = list(map(f,oo))

        elif exchange==exc.KUCOIN:
            oo = clients[exc.KUCOIN].get_active_orders_all(kv_format=True)
            b = oo['BUY']
            a = oo['SELL']
            l = list()
            for x in b: l.append(models.conv_openorder(x,exchange))
            for x in a: l.append(models.conv_openorder(x,exchange))
            oo = l

        elif exchange==exc.HITBTC:
            oo = clients[exchange].get_orders()
            f = lambda x: models.conv_openorder(x,exchange)
            oo = list(map(f,oo))
            return oo


        n = exc.NAMES[exchange]
        #log.info("open orders " + str(n) + " " + str(oo))
        return oo    

    # --- facade data ---    

    def all_open_orders(self, exchanges):
        oo = list()
        for e in exchanges:
            z = self.open_orders(e)
            n = exc.NAMES[e]
            for x in z:
                x['exchange'] = n
                oo.append(x)
            
        log.info("all open orders " + str(oo))
        return oo  

    def all_balance(self, exchanges):        
        bl = list()
        for e in exchanges:
            z = self.balance_all(e)
            n = exc.NAMES[e]
            for x in z:
                x['exchange'] = n
                bl.append(x)
        log.info("balance all %s"%(str(bl)))
        return bl

    # --- actions ---
        
    def submit_order(self, order, exchange=None):
        """ submit order which is array [type,order,qty] """
        # ("order " + str(order))         
        if exchange is None: exchange=self.s_exchange
        log.info("submit order " + str(exchange) + " " + str(order))
        market,ttype,order_price,qty = order

        if exchange==exc.CRYPTOPIA:            
            if ttype == "BUY":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "BUY", order_price, qty)
                if err:
                    log.error("! error with order " + str(order) + " " + str(err))
                else:
                    log.info("result " + str(result))
                    return result
            elif ttype == "SELL":
                result, err = clients[exc.CRYPTOPIA].submit_trade(market, "SELL", order_price, qty)
                if err:
                    log.error("error order " + str(order))
                else:
                    log.info("result " + str(result))
                    log.info("result " + str(result))

        elif exchange==exc.BITTREX:
            if ttype == "BUY":
                result = clients[exc.BITTREX].buy_limit(market, qty, order_price)
                log.info("order result %s" %str(result))
                return result
            elif ttype == "SELL":
                r = clients[exc.BITTREX].sell_limit(market, qty, order_price)
                log.info("order result %s" %str(r))
                return r

        elif exchange==exc.KUCOIN:
            c = clients[exc.KUCOIN]
            if ttype == "BUY":
                r = c.create_buy_order(market, order_price, qty)
                log.info("order result %s" %str(r))
                return r
            elif ttype == "SELL":
                r = c.create_sell_order(market, order_price, qty)
                log.info("order result %s" %str(r))
                return r

        elif exchange==exc.HITBTC:
            client = clients[exchange]
            r = int(random.random()*10000)
            oid = str(12341235+r)
            print ("submit ", oid, " ", market)
            if ttype=="BUY": 
                ttype="buy"
            else:
                ttype="sell"
            
            result = client.submit_order(oid, market, ttype, qty, order_price)
            print (result)


        """
        def submit_order(self, pair, side, qty, price):
        return self.submit_order(pair, "buy", qty, price)
        """
            

    def submit_order_check(self, order):
        """ submit order but require user action """
        # ("order " + str(order))
        result = ask_user("submit order " + str(order)+ " ? ")
        if result:
            self.submit(order)
        else:
            pass

    def cancel(self, order, exchange):
        """ cancel by order """
        if exchange is None: exchange=self.s_exchange
        result = None
        oid = order['oid']
        market = order['market']
        otype = order['otype']       
        log.info("cancel " + str(order)) 
        log.info("cancel " + str(oid) + " " + str(exchange) + " " + str(otype) + " " + str(market))
        
        if exchange==exc.CRYPTOPIA:            
            result,err = clients[exc.CRYPTOPIA].cancel_trade_id(oid)
            
        elif exchange==exc.BITTREX:
            result = clients[exc.BITTREX].cancel(oid)
            log.info("bitrex " + str(result))

        elif exchange==exc.KUCOIN:
            symbol = models.conv_markets_from(market, exchange)
            if otype == 'bid':                
                f = "BUY"
            else:
                f = "SELL"   
            result = clients[exc.KUCOIN].cancel_order(oid,f,symbol)                        
                
        
        log.info("result " + str(result))
        return result

    def cancel_id(self, oid, otype=None, market=None, exchange=None):
        """ cancel by id """
        if exchange is None: exchange=self.s_exchange            
        log.info("cancel! " + str(oid) + " " + str(exchange) + " " + str(otype))
        result = None
        if exchange==exc.CRYPTOPIA:            
            result,err = clients[exc.CRYPTOPIA].cancel_trade_id(oid)
            
        elif exchange==exc.BITTREX:
            result = clients[exc.BITTREX].cancel(oid)
            

        elif exchange==exc.KUCOIN:
            order_type = otype
            market = models.conv_markets_from(market, exchange)
            log.info("cancel! " + str(oid) + " " + str(exchange) + " " + str(otype) + " " + str(market))
            print ("!! CANCEL ",market)
            result = clients[exc.KUCOIN].cancel_order(oid,order_type,market)
        
        elif exchange==exc.HITBTC:
            result = clients[exchange].cancel_order(oid)

        else:
            log.error("no exchange provided")

        log.info("result " + str(result))
        return result

    def get_deposits(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            deposit_txs, _ = client.get_transactions("Deposit")
            return deposit_txs
        elif exchange==exc.BITTREX:            
            deposit_txs = client.get_deposit_history()["result"]
            return deposit_txs

    def get_funding(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            deposit_txs, _ = client.get_transactions("Deposit")
            withdraw_txs,_ = client.get_transactions("Withdraw")
            return deposit_txs + withdraw_txs
        elif exchange==exc.BITTREX:            
            deposit_txs = client.get_deposit_history()["result"]
            withdraw_txs = client.get_withdrawal_history()["result"]
            return deposit_txs + withdraw_txs

    # --- public info ---

    def market_history(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_history(market)
            return txs

        elif exchange==exc.BITTREX:
            r = clients[exc.BITTREX].get_market_history(market)
            r =r["result"]
            return r

        elif exchange==exc.KUCOIN:
            #res = client.RESOLUTION_1MINUTE
            #klines = client.get_historical_klines_tv(market, res, '1 hour ago UTC')            
            tx = client.get_recent_trades(market,limit=500)
            f = lambda x: models.convert_tx(x, exchange, market)
            tx = list(map(f,tx))  
            return tx

    def get_orderbook(self, market, exchange=None):
        if exchange is None: exchange=self.s_exchange
        log.debug ("get orderbook " + str(market))
        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            book, err = client.get_orders(market)
            if err:
                log.error ("error " + str(err))
            else:
                book = models.conv_orderbook(book, exchange)
                return book

        elif exchange==exc.BITTREX:            
            book = client.get_orderbook(market)["result"]            
            book = models.conv_orderbook(book, exchange)
            return book

        elif exchange==exc.KUCOIN:
            ob = client.get_order_book(market,limit=20)
            book = models.conv_orderbook(ob, exchange)
            #timestamp
            return book

    def get_market_summary(self, market, exchange):        
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]        
        if exchange==exc.CRYPTOPIA:
            result, err = client.get_market(market)
            r = models.conv_summary(result, exchange)
            return r
        elif exchange==exc.BITTREX:  
            s =  client.get_market_summary(market)["result"][0]
            r = models.conv_summary(s, exchange)
            return r
        elif exchange==exc.KUCOIN:
            r = models.conv_summary(client.get_tick(market),exchange)
            return r
        elif exchange==exc.HITBTC:
            r = client.get_ticker(market)
            r = models.conv_summary(r, exchange)
            return r


    def get_market_summaries(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            r = client.get_markets()[0]            
            f = lambda x: models.conv_summary(x,exchange)
            markets = [f(x) for x in r]
            #TODO use object
            return markets
        elif exchange==exc.BITTREX:   
            r = client.get_market_summaries()['result']
            f = lambda x: models.conv_summary(x, exchange)            
            #rex_markets = [x['MarketName'] for x in r]
            markets = [f(x) for x in r]
            #rex_markets = [Market(x,exc.BITTREX) for x in rex_markets]
            return markets
        elif exchange==exc.KUCOIN:
            r = client.get_tick()
            f = lambda x: models.conv_summary(x, exchange)  
            markets = [f(x) for x in r]          
            markets = list(filter(lambda x: x != None, markets))
            return markets
        elif exchange==exc.HITBTC:
            r = client.get_tickers()
            f = lambda x: models.conv_summary(x, exchange)  
            markets = list()
            for z in r:
                converted = f(z)
                if converted is not None:
                    markets.append(converted)            
            return markets

    def get_market_summaries_only(self, exchange=None):
        if exchange is None: exchange=self.s_exchange
        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            r = client.get_markets()[0]
            f = lambda x: models.conv_markets_to(x, exchange)
            cc_markets = [f(x['Label']) for x in r]
            #TODO use object
            return cc_markets
        elif exchange==exc.BITTREX:   
            r = client.get_market_summaries()['result']
            f = lambda x: models.conv_markets_to(x, exchange)            
            rex_markets = [x['MarketName'] for x in r]
            rex_markets = [f(x) for x in rex_markets]
            #rex_markets = [Market(x,exc.BITTREX) for x in rex_markets]
            return rex_markets

    def get_assets(self, exchange):
        client = clients[exchange]
        if exchange == exc.CRYPTOPIA:
            r,err = client.get_currencies()
            return r
        elif exchange==exc.BITTREX:   
            r = client.get_currencies()
            return r["result"]
        elif exchange==exc.KUCOIN:
            r = client.get_currencies()
            return r
        #elif exchange==exc.HITBTC:
