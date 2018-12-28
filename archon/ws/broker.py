from archon.config import *
import archon.facade as facade
import archon.exchange.exchanges as exc
import time
from archon.model import models
from pymongo import MongoClient
import datetime
from archon.feeds import cryptocompare
from archon.util import *

import logging
from loguru import logger


    
class WSBroker:
    """ 
    communitates with broker
    keeps datastructures in memory
    """

    def __init__(self):

        logger.start("log/broker.log", rotation="500 MB")

        logger.debug("init arch")

        filename = "apikeys.toml"
        self.afacade = facade.Facade()
        #in memory data
        self.balances = None
        self.openorders = list()
        self.submitted_orders = list()
        self.active_exchanges = list()
        self.selected_exchange = None

        self.set_keys_exchange_file()

        try:
            all_conf = parse_toml("conf.toml")
            #active_exchanges = all_conf["BROKER"]["active_exchanges"]
            #self.set_active_exchanges_name(active_exchanges)

            mongo_conf = all_conf["MONGO"]
            #mongoHost = mongo_conf['host']
            dbName = mongo_conf['db']        
            url = mongo_conf["url"]
            self.set_mongo(url, dbName)
        except:
            logger.error("no conf.toml file")

        self.starttime = datetime.datetime.utcnow()

        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        
    def set_mongo(self, url, dbName):
        #self.mongoHost = mongoHost
        #self.mongoPort = mongoPort
        self.mongo_url = url
        logger.debug("using mongo " + str(url))
        self.mongoclient = MongoClient(self.mongo_url)
        logger.debug("db %s"%dbName)
        self.db = self.mongoclient[dbName]

    def get_db(self):
        return self.db

    def set_active_exchanges(self, exchanges):
        logger.debug("set active exchanges %s"%exchanges)
        self.active_exchanges = exchanges  

    def set_active_exchanges_name(self, exchanges_names):
        ne = list()
        for n in exchanges_names:
            eid = exc.get_id(n)
            ne.append(eid)
        self.active_exchanges = ne

    def set_keys_exchange_file(self,keys_filename="apikeys.toml"):
        try:
            apikeys = parse_toml(keys_filename)
            logger.info("set keys %s"%apikeys.keys())
            if not self.active_exchanges:
                ae = list()
                for k,v in apikeys.items():
                    eid = exc.get_id(k)
                    if eid >= 0:
                        try:
                            self.set_keys_exchange(eid, apikeys[k])
                            ae.append(eid)
                        except Exception as err:
                            logger.error("could not set %s"%err)
                    else:
                        logger.error ("exchange not supported or not set")
                logger.info("active exchanges %s"%ae)
            else:
                logger.error("active exchanages already set")
                
        except Exception as err: 
            logger.error("error parsing apikeys file %s"%(err))
            

    def set_keys_exchange(self, exchange, keys):
        pubkey = keys["public_key"]
        secret = keys["secret"]
        logger.debug ("set keys %i %s"%(exchange,keys['public_key']))
        #self.db.apikeys.save({"exchange":exchange,"pubkey":pubkey,"secret":secret})
        self.afacade.set_api_keys(exchange, pubkey, secret)
        self.active_exchanges.append(exchange)

    def get_active_exchanges(self):
        return self.active_exchanges

    def get_apikeys_all(self):
        return list(self.db.apikeys.find())
    
    def sync_orders(self):
        oo = self.global_openorders()
        logger.info("sync orders %s"%oo)
        self.openorders = oo

    def get_by_id(self, oid):
        x = list(filter(lambda x: x['oid'] == oid, self.openorders))
        return x[0]

    # --- broker data ---    

    def global_openorders(self):
        oo = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            logger.info("%i %s"%(e,n))
            z = self.afacade.open_orders(e)
            if z:                                
                if len(z) > 0:
                    for x in z:
                        x['exchange'] = n
                        oo.append(x)
            
        logger.debug("all open orders " + str(oo))
        return oo  

    """
    def all_balance(self):        
        bl = list()
        for e in self.active_exchanges:
            logger.debug("get balance ",e)
            z = self.afacade.balance_all(e)
            logger.debug(z,e)
            n = exc.NAMES[e]
            for x in z:
                x['exchange'] = n
                bl.append(x)
        logger.debug("balance all %s"%(str(bl)))
        return bl
    """

    def global_balances(self):
        """ a list of balances by currency and exchange """
        bl = list()
        logger.debug("active exchanges %s"%(self.active_exchanges))
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            b = self.afacade.balance_all(exchange=e)
            if b == None: 
                logger.error("could not fetch balances from %s"%n)
            for x in b:
                x['exchange'] = n
                s = x['symbol']
                t = float(x['amount'])
                bl.append(x)
        return bl

    def global_balances_usd(self):
        bl = self.global_balances()
        for x in bl:
            s = x['symbol']
            usd_price = cryptocompare.get_usd(s)    
            x['USDprice'] = usd_price        
            x['USDvalue'] = round(t*usd_price,2)                
            #if x['USDvalue'] > 1:                
        return bl

    def global_tradehistory(self):
        txlist = list()
        for e in self.active_exchanges:
            if e == exc.BINANCE:
                #TODO use balances instead
                #markets = self.fetch_global_markets(denom='BTC')
                b = self.afacade.balance_all(exc.BINANCE)
                alltx = list()
                for m in b:
                    s = m['symbol']
                    if s == 'BTC': continue
                    if s == 'USDT': continue
                    ms = models.get_market(m['symbol'],"BTC",exc.BINANCE)
                    
                    tx = self.afacade.trade_history(market=ms,exchange=e)
                    alltx += tx
                txlist += alltx                    
            else:
                n = exc.NAMES[e]
                logger.info("get %s"%n)
                tx = self.afacade.get_tradehistory_all(exchange=e)
                if tx != None:
                    for x in tx:
                        x["exchange"] = n
                        txlist.append(x)
        return txlist

    #TODO             
    def submit_order(self, order, exchange=None):
        if exchange is None: exchange=self.selected_exchange
        #TODO check balance before submit
        market,ttype,order_price,qty = order
        self.submitted_orders.append(order)
        [order_result,order_success] = self.afacade.submit_order(order, exchange)
        logger.info("order result %s"%order_result)


    def cancel_order(self, oid):                
        order = self.get_by_id(oid)
        #oid, otype=None,exchange=None,symbol=None):
        oid, otype,exchange, market = order['oid'],order['otype'],order['exchange'],order['market']
        exchange = exc.get_id(exchange)
        self.afacade.cancel_id(oid, otype, market, exchange)

    def cancel_all(self, exchange=None):
        #logger.info("cancel all")
        if exchange is None: exchange=self.selected_exchange
        self.sync_orders()
        for o in self.openorders:
            logger.info("cancel " + str(o))
            self.cancel_order(o['oid'])
        
    def fetch_global_markets(self,denom=None):
        binance_blocked = ['HSR','VEN']
        allmarkets = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            logger.info("fetch %s"%n)
            m = self.afacade.get_market_summaries(e)
            for x in m:
                x['exchange'] = n
            
            if denom:
                filtered = list()
                f = lambda x: x['denom']=='BTC'
                m = list(filter(f, m))            

                f = lambda x: x['nom'] not in binance_blocked
                m = list(filter(f, m))            
                allmarkets += m
            else:
                allmarkets += m
        return allmarkets

    def aggregate_book(self, books):
        allbids = list()
        allasks = list()
        ts = None
        for z in books:
            b = z['bids']
            allbids += b
            a = z['asks']
            allasks += a
            ts = z['timestamp']
        allbids = sorted(allbids, key=lambda k: k['price'])
        allbids.reverse()
        allasks = sorted(allasks, key=lambda k: k['price'])
        return [allbids,allasks,ts]

    def global_orderbook(self, market):
        #self.db.orderbooks.drop()
        logger.info("global orderbook for %s"%market)
        allbids = list()
        allasks = list()
        ts = None
        for e in self.active_exchanges:            
            n = exc.NAMES[e]
            x = self.db.orderbooks.find({'market':market,'exchange':n})            
            for z in x:
                b = z['bids']
                for xb in b: xb['exchange'] = n
                allbids += b

                a = z['asks']
                for xb in a: xb['exchange'] = n
                allasks += a
                ts = z['timestamp']

        allbids = sorted(allbids, key=lambda k: k['price'])
        allbids.reverse()        
        allasks = sorted(allasks, key=lambda k: k['price'])
        return [allbids,allasks,ts]

    def global_txhistory(self, market):
        tx_all = list()
        for e in self.active_exchanges:            
            n = exc.NAMES[e]
            txs = a.afacade.market_history(market,e)
            for tx in txs:
                tx["exchange"] = n
                tx_all.append(tx)
        return tx_all

    def filter_markets(self, m):
        f = lambda x: markets.is_btc(x['pair'])
        m = list(filter(f, m))
        return m

    def get_markets(self,exchange=None,denom=None):
        f = {}
        if exchange:
            f = {'exchange':exchange}
        if denom:
            f['denom'] = denom
        m = list(self.db.markets.find(f))
        #else:
        #    m = list(self.db.markets.find())
        return m

    def get_candle(self, market):
        logger.debug("get candle " + market)
        result = self.db.candles.find_one({'market': market})        
        return result

    # sync functions

    def sync_orderbook(self, market, exchange):
        smarket = models.conv_markets_to(market, exchange)  
        logger.debug("sync %s %i"%(market,exchange))   
        #TODO check if symbol is supported by exchange   
        try:
            n = exc.NAMES[exchange]
            [bids,asks] = self.afacade.get_orderbook(smarket,exchange)
            dt = datetime.datetime.utcnow()
            x = {'market': market, 'exchange': n, 'bids':bids,'asks':asks,'timestamp':dt}
            
            self.db.orderbooks.remove({'market':market,'exchange':n})
            self.db.orderbooks.insert(x)
            self.db.orderbooks_history.insert(x)
        except:
            logger.info("sync book failed. symbol not supported")

    def sync_orderbook_all(self, market):   
        self.db.orderbooks.drop()     
        for e in self.active_exchanges:            
            self.sync_orderbook(market, e) 

    def sync_balances(self):
        balances = self.global_balances()
        logger.info("insert %s"%balances)
        self.db.balances.drop()
        dt = datetime.datetime.utcnow()
        self.db.balances.insert({'balance_items':balances,'t':dt})
        self.db.balances_history.insert(balances)

    def latest_balances(self):
        b = self.db.balances.find_one()
        return b

    def get_global_orderbook(self, market):
        books = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            logger.info("global orderbook %s %s"%(n,market))
            #smarket = models.conv_markets_to(market, e)  
            try:
                
                [bids,asks] = self.afacade.get_orderbook(market,e)
                dt = datetime.datetime.utcnow()
                n = exc.NAMES[e]
                for xb in bids: xb['exchange'] = n
                for xa in asks: xa['exchange'] = n

                x = {'market': market, 'exchange': n, 'bids':bids,'asks':asks,'timestamp':dt}
                books.append(x)
            except Exception as err:
                logger.error("error global orderbook %i %s %s"%(e,market,err))
        [bids,asks,ts] = self.aggregate_book(books)
        return [bids,asks,ts]

    def sync_tx(self, market, exchange):
        try:            
            smarket = models.conv_markets_to(market, exchange)  
            txs = self.afacade.market_history(smarket,exchange)
            n = exc.NAMES[exchange]
            smarket = models.conv_markets_to(market, exchange)
            dt = datetime.datetime.utcnow()
            x = {'market': market, 'exchange': n, 'tx':txs,'timestamp':dt}
            self.db.txs.remove({'market':market,'exchange':n})
            self.db.txs.insert(x)     
            self.db.txs_history.insert(x)
        except:
            logger.error("symbol not supported")

    def sync_tx_all(self, market):              
        for e in self.active_exchanges:
            self.db.txs.remove({'market':market,'exchange':e})
            self.sync_tx(market, e)   

    def sync_markets_all(self):
        self.db.markets.drop()
        ms = self.fetch_global_markets()
        dt = datetime.datetime.utcnow()        
        nm = list()
        for x in ms:
            try:
                dts = dt.strftime('%H:%M:%S')
                x['timestamp'] = dts
                n,d = x['pair'].split('_')
                x['nom'] = n
                x['denom'] = d   
                self.db.markets.insert(x)
                self.db.markets_history.insert(x)
            except:
                pass

    def sync_candle_daily(self, market, exchange):
        logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_daily(market, exchange)
        n = exc.NAMES[exchange]
        n,d = market.split('_')
        self.db.candles.insert({"exchange":n,"market":market,"nom":n,"denom":d,"candles":candles,"interval": "1d"})

    def sync_candle_minute(self, market, exchange):
        logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_minute(market, exchange)
        n = exc.NAMES[exchange]
        n,d = market.split('_')
        dt = datetime.datetime.utcnow()        
        dts = dt.strftime('%H:%M:%S')        
        self.db.candles.insert({"exchange":n,"market":market,"nom":n,"denom":d,"candles":candles,"interval": "1m", "time_insert":dts})
        
    def sync_candle_minute15(self, market, exchange):
        logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_minute15(market, exchange)
        n = exc.NAMES[exchange]
        n,d = market.split('_')
        dt = datetime.datetime.utcnow()        
        dts = dt.strftime('%H:%M:%S')        
        self.db.candles.insert({"exchange":n,"market":market,"nom":n,"denom":d,"candles":candles,"interval": "1m", "time_insert":dts})

    def sync_candles_all(self, market):
        for e in self.active_exchanges:            
            self.sync_candle_daily(market, e)   

    def sync_candle_daily_all(self):
        ms = self.fetch_global_markets()
        logger.info(len(ms))

        #cndl = self.afacade.get_candles_daily(market,exc.BINANCE)

        for x in ms[:]:
            market = x['pair']
            logger.info("sync %s"%market)
            try:
                self.sync_candle_daily(market,exc.BINANCE)
            except:
                pass


        #for e in self.active_exchanges:            
        #    #self.sync_candle_daily(market, e)   



    def transaction_queue(self,exchange):
        now = datetime.datetime.utcnow()
        #delta = now - self.starttime
        txs = self.afacade.get_tradehistory_all(exchange)
        for tx in txs[:]:
            ts = tx['timestamp'][:19]
            dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')        
            if dt > self.starttime:
                logger.info("new tx")
            
