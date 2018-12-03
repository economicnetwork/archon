"""
broker

unified interface to exchanges
broker takes care of the translating logic in models
functions take exchange as the parameters and are forwarded to the exchange
"""

import archon.exchange.exchanges as exc
from archon.util import *
from archon.model import models

#Wrappers
import archon.exchange.rex as bittrex
from archon.exchange.cryptopia import CryptopiaAPI
from archon.exchange.kucoin import KuClient
import archon.exchange.hitbtc as hitbtc
import archon.exchange.binance as binance

#Wrappers with foreign package
import krakenex

import time
import sys
import time
import random
import json


clients = {}

logpath = './log'
log = setup_logger(logpath, 'broker_logger', 'broker')

rex_API_v2= "rex_API_v2"
 
class Broker:

    def __init__(self):
        log.info("init broker")

    def set_api_keys(self, exchange, key, secret):
        """ set clients, assumes conf file present """
        log.debug("set api " + str(exchange))
        if exchange==exc.CRYPTOPIA:
            clients[exchange] = CryptopiaAPI(key, secret)
        elif exchange==exc.BITTREX:
            clients[exchange] = bittrex.Bittrex(key,secret)
            #maintain version for candles
            clients[rex_API_v2] = bittrex.Bittrex(key,secret,api_version=bittrex.API_V2_0)  
        elif exchange==exc.KUCOIN:
            clients[exchange] = KuClient(key,secret)   
        elif exchange==exc.HITBTC:
            clients[exchange] = hitbtc.RestClient(key,secret)   
        elif exchange==exc.BINANCE:
            clients[exchange] = binance.Client(key,secret)
        elif exchange==exc.KRAKEN:        
            clients[exchange] = krakenex.API(key,secret)

    def set_mail_config(self, apikey, domain, email_from, email_to):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain
        self.email_from = email_from
        self.email_to = email_to

    def get_client(self, EXC):
        """ directly get a client """
        return clients[EXC]


    # --- public info ---

    def exchange_status(self):
        status = {}
        for e in self.active_exchanges:
            try:
                self.balance_all(e)
                status[e] = "connected"
            except:
                status[e] = "disconnected"


    def market_history(self, market, exchange=None):

        client = clients[exchange]
        if exchange==exc.CRYPTOPIA:
            txs, _ = clients[exc.CRYPTOPIA].get_history(market)
            f = lambda x: models.conv_tx(x, exchange, market)
            txs = list(map(f,txs))
            return txs
        elif exchange==exc.BITTREX:
            r = clients[exc.BITTREX].get_market_history(market)
            txs = r["result"]
            f = lambda x: models.conv_tx(x, exchange, market)
            txs = list(map(f,txs))
            return txs
        elif exchange==exc.KUCOIN:
            tx = client.get_recent_trades(market,limit=50)
            f = lambda x: models.conv_tx(x, exchange, market)
            tx = list(map(f,tx))  
            return tx

    def get_orderbook(self, market, exchange=None):
        client = clients[exchange]
        market = models.conv_markets_to(market, exchange)
        log.debug("get orderbook %s %i" %(str(market),exchange))

        if exchange==exc.CRYPTOPIA:
            book, err = client.get_orders(market)
            if err:
                log.error ("error " + str(err))
            else:
                book = models.conv_orderbook(book, exchange)
                return book
        elif exchange==exc.BITTREX:            
            try:
                book = client.get_orderbook(market)["result"]            
                book = models.conv_orderbook(book, exchange)
                return book
            except:
                log.error("error fetching orderbook",exchange)
        elif exchange==exc.KUCOIN:
            try:
                ob = client.get_order_book(market,limit=20)
                book = models.conv_orderbook(ob, exchange)
                #timestamp
                return book
            except Exception:
                 raise Exception
        elif exchange==exc.HITBTC:
            try:
                ob = client.get_orderbook(market)
                book = models.conv_orderbook(ob, exchange)
                return book
            except:
                log.error("error fetching orderbook",exchange)

        elif exchange==exc.KRAKEN:
            response = client.query_public('Depth', {'pair': market, 'count': '100'})
            r = list(response['result'].values())[0]
            book = models.conv_orderbook(r, exchange)
            return book

        elif exchange==exc.BINANCE:
            log.info("get orderbook %s"%(market))
            try:
                ob = client.get_orderbook_symbol(market)
                book = models.conv_orderbook(ob, exchange)
                return book
            except Exception:
                 raise Exception

    def get_market_summary(self, market, exchange):        

        client = clients[exchange] 
        market = models.conv_markets_to(market, exchange)       
        if exchange==exc.CRYPTOPIA:
            r, err = client.get_market(market)
            r = models.conv_summary(r, exchange)
            return r
        elif exchange==exc.BITTREX:  
            r = client.get_market_summary(market)["result"][0]
            r = models.conv_summary(r, exchange)
            return r
        elif exchange==exc.KUCOIN:
            r = client.get_tick(market)
            c = models.conv_summary(r,exchange)
            return c
        elif exchange==exc.HITBTC:
            r = client.get_ticker(market)
            r = models.conv_summary(r, exchange)
            return r
        elif exchange==exc.BINANCE:
            r = client.get_orderbook_ticker_symbol(market)
            r = models.conv_summary(r, exchange)
            return r


    def get_market_summaries(self, exchange=None):

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            r = client.get_markets()
            f = lambda x: models.conv_summary(x,exchange)
            markets = [f(x) for x in r]
            markets = list(filter(lambda x: x != None, markets))
            return markets

        elif exchange==exc.BITTREX:   
            r = client.get_market_summaries()['result']
            f = lambda x: models.conv_summary(x, exchange)            
            markets = [f(x) for x in r]
            markets = list(filter(lambda x: x != None, markets))
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
            markets = list(filter(lambda x: x != None, markets))         
            return markets

        elif exchange==exc.BINANCE:
            r = client.get_ticker()
            f = lambda x: models.conv_summary(x, exchange)
            markets = [f(x) for x in r]          
            markets = list(filter(lambda x: x != None, markets))            
            return markets
            

    def get_market_summaries_only(self, exchange=None):

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

    def market_id_map(self, exchange):
        #cryptocopia
        client = clients[exchange]
        m = client.get_markets()
        d = {}
        for z in m:
            l = z['Label']
            market = models.conv_markets_from(l, exchange)
            p = z['TradePairId']
            d[market] = p
        return d

    def get_candles_daily(self, market, exchange):
        client = clients[exchange]

        if exchange == exc.CRYPTOPIA:
            d = self.market_id_map(exchange)
            pairid = d[market]
            candles, v = client.candle_request(pairid)
            return models.conv_candle([candles,v],exchange)
            
        elif exchange==exc.BITTREX: 
            market = models.conv_markets_to(market, exchange)  
            #hack second client for candles
            r = clients[rex_API_v2].get_candles(market,"day")
            r = r['result']
            candles = models.conv_candle(r, exchange)
            return candles

        elif exchange==exc.KUCOIN:
            market = models.conv_markets_to(market, exchange)
            klines = client.get_historical_klines_tv(market, client.RESOLUTION_1DAY, '1 month ago UTC')    
            return models.conv_candle(klines,exchange)  

        elif exchange==exc.HITBTC:
            market = models.conv_markets_to(market, exchange)
            candles = client.get_candles_daily(market)
            candles = models.conv_candle(candles, exchange)
            return candles
        
        elif exchange==exc.BINANCE:
            market = models.conv_markets_to(market, exchange)
            klines = client.get_candles_daily(market)    
            return models.conv_candle(klines,exchange)

    def get_candles_hourly(self, market, exchange):
        client = clients[exchange]

        if exchange == exc.CRYPTOPIA:
            pass            
        elif exchange==exc.BITTREX:   
            market = models.conv_markets_to(market, exchange)
            r = clients[rex_API_v2].get_candles(market,"hour")
            r = r['result']
            candles = models.conv_candle(r, exchange)
            return candles
        elif exchange==exc.KUCOIN:
            market = models.conv_markets_to(market, exchange)
            klines = client.get_historical_klines_tv(market, client.RESOLUTION_1HOUR, '1 week ago UTC')    
            return models.conv_candle(klines,exchange)

        elif exchange==exc.BINANCE:
            market = models.conv_markets_to(market, exchange)
            klines = client.get_candles_hourly(market)    
            return models.conv_candle(klines,exchange)


    def get_candles_minute(self, market, exchange):
        client = clients[exchange]
        market = models.conv_markets_to(market, exchange)

        if exchange == exc.CRYPTOPIA:
            pass            

        elif exchange==exc.BITTREX:            
            r = clients[rex_API_v2].get_candles(market,"oneMin")
            r = r['result']
            candles = models.conv_candle(r, exchange)
            return candles

        elif exchange==exc.KUCOIN:
            klines = client.get_historical_klines_tv(market, client.RESOLUTION_1MINUTE, '1 day ago UTC')
            return models.conv_candle(klines,exchange)

    def get_latest_candle(self, market, exchange):
        pass
        #get_latest_candle                    

    # --- trading info ---

    def balance_all(self, exchange=None):
        log.info("balance")

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            b, error = clients[exc.CRYPTOPIA].get_balance_all()        
            b = models.conv_balance(b,exchange)
            return b
        
        elif exchange==exc.BITTREX:
            r = clients[exc.BITTREX].get_balances()
            b = r["result"]
            b = models.conv_balance(b,exchange) 
            return b

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
            r = clients[exc.KRAKEN].query_private('Balance')
            b = r['result']
            b = models.conv_balance(b,exchange) 
            return b

    def balance_currency(self, currency, exchange=None):
        """ Deprecated: use balance all """
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

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            txs, _ = client.get_tradehistory(market)
            return txs

        elif exchange==exc.BITTREX:
            r = client.get_market_history(market)['result']            
            f = lambda x: models.conv_usertx(x,exchange)
            r = list(map(f,r))
            return r

        elif exchange==exc.KUCOIN:
            r = client.get_dealt_orders(limit=500)
            f = lambda x: models.conv_usertx(x,exchange)
            r = list(map(f,r))
            return r

        elif exchange==exc.HITBTC:
            pass

        elif exchange==exc.BINANCE:
            tx = client.get_my_trades(symbol=market)
            f = lambda x: models.conv_usertx(x,exchange)
            r = list(map(f,tx))
            return r
            
    def get_tradehistory_all(self, exchange=None):

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            txs, err = client.get_tradehistory_all()
            f = lambda x: models.conv_usertx(x,exchange)
            txs = list(map(f,txs))
            return txs

        elif exchange==exc.BITTREX:
            txs = client.get_order_history()
            f = lambda x: models.conv_usertx(x,exchange)
            txs = list(map(f,txs))
            return txs

        elif exchange==exc.KUCOIN:
            r = client.get_dealt_orders(limit=100)['datas']
            f = lambda x: models.conv_usertx(x,exchange)
            txs = list(map(f,r))
            return txs

        elif exchange==exc.HITBTC:
            pass

        elif exchange==exc.BINANCE:
            pass
            #get_my_trades

    def open_orders_symbol(self, symbol, exchange=None):

        oo = None
        symbol = models.conv_markets_to(symbol, exchange)
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

        elif exchange==exc.BINANCE:
            oo = clients[exc.BINANCE].get_open_orders()            
            f = lambda x: models.conv_openorder(x,exchange)
            oo = list(map(f,oo))

        n = exc.NAMES[exchange]
        #log.info("open orders " + str(n) + " " + str(oo))
        return oo    

    # --- actions ---
        
    def submit_order(self, order, exchange=None):
        """ submit order which is array [type,order,qty] """
        # ("order " + str(order))         

        log.info("submit order " + str(exchange) + " " + str(order))
        market,ttype,order_price,qty = order
        market = models.conv_markets_to(market, exchange)
        client = clients[exchange]

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
            
            r = int(random.random()*10000)
            oid = str(12341235+r)
            #log.info("submit %s %s"%(str(oid),str(market)))
            log.info("submit " + str(oid) + " " + str(market))
            if ttype=="BUY": 
                ttype="buy"
            else:
                ttype="sell"
            
            result = client.submit_order(oid, market, ttype, qty, order_price)
            log.info("order result %s"%str(result))
            return result

        elif exchange==exc.BINANCE:
            log.info("submit %s"%order)
            if ttype=="BUY":
                r = client.submit_order_buy(market, qty, order_price)
            else:
                r = client.submit_order_sell(market, qty, order_price)
            print (r)
            return r


    def submit_order_check(self, order):
        """ submit order but require user action """
        result = ask_user("submit order " + str(order)+ " ? ")
        if result:
            self.submit_order(order)
        else:
            pass

    def cancel(self, order):
        """ cancel by order """
        #if exchange is None: exchange=self.s_exchange
        e = order['exchange']
        exchange = exc.get_id(e)
        result = None
        oid = order['oid']
        market = order['market']
        otype = order['otype']       
        #log.info("cancel " + str(order)) 
        log.info("cancel " + str(oid) + " " + str(e) + " " + str(otype) + " " + str(market))
        
        if exchange==exc.CRYPTOPIA:            
            result,err = clients[exc.CRYPTOPIA].cancel_trade_id(oid)
            
        elif exchange==exc.BITTREX:
            result = clients[exc.BITTREX].cancel(oid)
            log.info("bitrex " + str(result))

        elif exchange==exc.KUCOIN:
            symbol = models.conv_markets_to(market, exchange)
            if otype == 'bid':                
                f = "BUY"
            else:
                f = "SELL"   
            log.info("cancel ",symbol,oid,f)
            result = clients[exc.KUCOIN].cancel_order(oid,f,symbol)      
            return result                  
                        
        elif exchange==exc.HITBTC:
            result = clients[exc.HITBTC].cancel_order(oid)
                    
        log.debug("result " + str(result))
        return result

    def cancel_id(self, oid, otype=None, market=None, exchange=None):
        """ cancel by id """
            
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
            result = clients[exc.KUCOIN].cancel_order(oid,order_type,market)
        
        elif exchange==exc.HITBTC:
            result = clients[exchange].cancel_order(oid)

        elif exchange == exc.BINANCE:
            result = clients[exchange].cancel_order(symbol=market,orderId=oid)

        else:
            log.error("no exchange provided")

        log.info("result " + str(result))
        return result

    def get_deposits(self, exchange=None):

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            deposit_txs, _ = client.get_transactions("Deposit")
            return deposit_txs

        elif exchange==exc.BITTREX:            
            deposit_txs = client.get_deposit_history()["result"]
            return deposit_txs

    def get_funding(self, exchange=None):

        client = clients[exchange]

        if exchange==exc.CRYPTOPIA:
            deposit_txs, _ = client.get_transactions("Deposit")
            withdraw_txs,_ = client.get_transactions("Withdraw")
            return deposit_txs + withdraw_txs
            
        elif exchange==exc.BITTREX:            
            deposit_txs = client.get_deposit_history()["result"]
            withdraw_txs = client.get_withdrawal_history()["result"]
            return deposit_txs + withdraw_txs
