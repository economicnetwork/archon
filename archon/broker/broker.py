"""
broker without middleware
"""

import datetime
import time
import logging
import os
from pathlib import Path
from pymongo import MongoClient

import archon.broker.facade as facade
import archon.exchange.exchanges as exc
import archon.util.orderbooks as orderbooks
from archon.broker.config import parse_toml
from archon.feeds import cryptocompare
from archon.model import models
import archon.exchange.bitmex.fields as bitmexfields
from archon.util.custom_logger import setup_logger

standard_apikeys_file = "apikeys.toml"

class Broker:
    """
    communicate with exchanges via facade
    keeps datastructures in memory
    single user broker
    """

    def __init__(self,setAuto=True,setMongo=True):

        setup_logger(logger_name="broker", log_file='broker.log')
        self.logger = logging.getLogger("broker")

        self.afacade = facade.Facade()
        #in memory data
        self.balances = None
        self.openorders = list()
        self.submitted_orders = list()
        self.active_exchanges = list()
        self.selected_exchange = None

        if setAuto:
            self.set_keys_exchange_file()

        if setMongo:
            try:
                wdir = self.get_workingdir()
                path_file_config = wdir + "/" + "config.toml"
                config_dict = parse_toml(path_file_config)
            except:
                self.logger.error("no file. path expected: %s"%str(path_file_config))
            try:
                mongo_conf = config_dict["MONGO"]
                uri = mongo_conf["uri"]
                self.set_mongo(uri)
                self.using_mongo = True
            except:
                self.using_mongo = False
                self.logger.error("could not set mongo")


        self.starttime = datetime.datetime.utcnow()

    def get_workingdir(self):
        home = str(Path.home())
        wdir = home + "/.archon"

        if not os.path.exists(wdir):
            os.makedirs(wdir)

        return wdir

    def set_mongo(self, uri):
        self.logger.debug("using mongo %s"%str(uri))
        mongoclient = MongoClient(uri)
        self.db = mongoclient["broker-db"]

    def get_db(self):
        return self.db
    
    def set_keys_exchange_file(self, path_file_apikeys=None, exchanges=None):
        self.logger.info("set_keys_exchange_file")
        if path_file_apikeys is None:
            wdir = self.get_workingdir()
            #standard_apikeys_file
            path_file_apikeys = wdir + "/" + standard_apikeys_file
        apikeys = parse_toml(path_file_apikeys)
        print(apikeys)
        self.logger.info("set keys %s"%apikeys.keys())
        import pdb
        #pdb.set_trace()
        if exchanges:
            for e in exchanges:
                try:
                    self.logger.info("set %s %s"%(e, str(apikeys[e])))
                    self.set_keys_exchange(e, apikeys[e])
                except Exception as err:
                    self.logger.error("could not set %s"%str(err))
        else:
            try:
                if not self.active_exchanges:
                    print (">> ",apikeys)
                    for k,v in apikeys.items():
                        if exc.exchange_exists(k):
                            try:
                                self.set_keys_exchange(k, apikeys[k])
                                self.active_exchanges.append(k)
                            except Exception as err:
                                self.logger.error("could not set %s"%err)
                        else:
                            self.logger.error ("exchange not supported or not set")
                    self.logger.info("active exchanges %s"%self.active_exchanges)

            except Exception as err:
                self.logger.error("error parsing apikeys file: %s"%(err))


    def set_keys_exchange(self, exchange, keys):
        pubkey = keys["public_key"]
        secret = keys["secret"]
        self.logger.info ("set keys %s %s"%(exchange,keys['public_key']))
        self.afacade.set_api_keys(exchange, pubkey, secret)

    def get_apikeys_all(self):
        return list(self.db.apikeys.find())

    def set_mail_config(self, apikey, domain):
        """ mailgun config """
        self.mail_api_key = apikey
        self.mail_domain = domain
        #self.email_from = email_from
        #self.email_to = email_to

    # --- bitmex specfic ---

    def margin_balance(self, e):
        if e == exc.BITMEX:
            n = exc.NAMES[e]
            client = self.afacade.get_client(exc.BITMEX)
            r = client.funds()
            mbal = r[bitmexfields.marginBalance]
            self.logger.info("margin balance %s"%mbal)
            return mbal


    # --- broker data ---

    def get_order_by_id(self, oid):
        x = list(filter(lambda x: x['oid'] == oid, self.openorders))
        return x[0]

    def global_openorders(self):
        oo = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            self.logger.info("%s %s"%(e,n))
            z = self.afacade.open_orders(e)
            if z:
                if len(z) > 0:
                    for x in z:
                        x['exchange'] = n
                        oo.append(x)

        self.logger.debug("all open orders " + str(oo))
        return oo

    def sync_orders(self):
        oo = self.global_openorders()
        self.logger.info("sync orders %s"%oo)
        self.openorders = oo

    def global_balances(self):
        """ a list of balances by currency and exchange """
        bl = list()
        self.logger.debug("active exchanges %s"%(self.active_exchanges))
        for e in self.active_exchanges:
            if e != exc.BITMEX:
                n = exc.NAMES[e]
                b = self.afacade.balance_all(exchange=e)
                if b == None:
                    self.logger.error("could not fetch balances from %s"%n)
                for x in b:
                    x['exchange'] = n
                    bl.append(x)
            else:
                self.logger.error("bitmex does not support balance call")
        return bl

    def global_balances_usd(self):
        bl = self.global_balances()
        for x in bl:
            s = x['symbol']
            usd_price = cryptocompare.get_usd(s)
            x['USDprice'] = usd_price
            x['USDvalue'] = round(t*usd_price,2)
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
                    if s == 'BTC': 
                        continue
                    if s == 'USDT': 
                        continue
                    ms = models.get_market(m['symbol'],"BTC",exc.BINANCE)

                    tx = self.afacade.trade_history(market=ms,exchange=e)
                    alltx += tx
                txlist += alltx
            else:
                n = exc.NAMES[e]
                self.logger.info("get %s"%n)
                tx = self.afacade.get_tradehistory_all(exchange=e)
                if tx != None:
                    for x in tx:
                        x["exchange"] = n
                        txlist.append(x)
        return txlist

    def submit_order(self, order, exchange=None):
        if exchange is None: exchange=self.selected_exchange
        if exchange!=exc.BITMEX:
            #TODO check balance before submit
            #market,ttype,order_price,qty = order
            self.log_submit_order(order)

            self.submitted_orders.append(order)
            [order_result,order_success] = self.afacade.submit_order(order, exchange)
            self.logger.info("order result %s"%order_result)
        else:
            [order_result,order_success] = self.afacade.submit_order(order, exchange)
            self.logger.info("order result %s"%order_result)

        return [order_result,order_success]

    def submit_order_post(self, order, exchange=None):

        if exchange!=exc.BITMEX:
            self.logger.error("post not supported")
            """

            #TODO check balance before submit
            #market,ttype,order_price,qty = order
            self.log_submit_order(order)

            self.submitted_orders.append(order)
            [order_result,order_success] = self.afacade.submit_order(order, exchange)
            self.logger.info("order result %s"%order_result)
            """
        elif exchange==exc.DERIBIT:
            self.logger.error("post not working")
        elif exchange==exc.BITMEX:
            [order_result,order_success] = self.afacade.submit_order_post(order, exchange)
            self.logger.info("order result %s"%order_result)

        return [order_result,order_success]


    def __old_cancel_order(self, oid):
        self.logger.debug("cancel %s"%str(oid))
        #TODO check order exists
        order = self.get_by_id(oid)
        #oid, otype=None,exchange=None,symbol=None):
        oid, otype,exchange, market = order['oid'],order['otype'],order['exchange'],order['market']
        exchange = exc.get_id(exchange)
        self.afacade.cancel_id(oid, otype, market, exchange)

    def cancel_order(self, oid, exchange):
        self.logger.debug("cancel %s"%str(oid))
        self.log_cancel_order(oid)
        result = self.afacade.cancel_id(oid, exchange=exchange)
        return result

    def cancel_all(self, exchange=None):
        self.logger.debug("cancel all")
        if exchange is None: exchange=self.selected_exchange
        self.sync_orders()
        for o in self.openorders:
            self.logger.info("cancel " + str(o))
            self.cancel_order(o['oid'])

    def fetch_global_markets(self,denom=None):
        #temporary workaround for broken binance symbols
        binance_blocked = ['HSR','VEN']
        allmarkets = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            self.logger.info("fetch %s"%n)
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

    def global_orderbook(self, market):
        #self.db.orderbooks.drop()
        self.logger.info("global orderbook for %s"%market)
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
        self.logger.debug("get candle " + market)
        result = self.db.candles.find_one({'market': market})
        return result

    # --- sync functions ---

    def sync_orderbook(self, market, exchange):
        #smarket = models.conv_markets_to(market, exchange)
        self.logger.debug("sync %s %s"%(market,exchange))
        #TODO check if symbol is supported by exchange
        try:
            n = exc.NAMES[exchange]

            book = self.afacade.get_orderbook(market,exchange)
            dt = datetime.datetime.utcnow()
            #x = {'market': market, 'exchange': n, 'bids':bids,'asks':asks,'timestamp':dt}
            book['exchange'] = n

            self.logger.debug("sync %s"%str(dt))
            #TODO don't remove
            #self.db.orderbooks.remove({'market':market,'exchange':n})
            self.db.orderbooks.insert(book)
            #self.db.orderbooks_history.insert(book)
        except Exception as e:
            self.logger.info("sync book failed %s"%e)

    def sync_trades(self, market, exchange):
        if exchange == exc.BITMEX:
            try:
                trades = self.afacade.market_history(market, exchange)
                #self.logger.debug("trades %s"%str(trades))
                self.db.trades.insert(trades)
            except Exception as e:
                self.logger.info("sync trades failed %s"%str(e))

    def sync_orderbook_all(self, market):
        self.db.orderbooks.drop()
        for e in self.active_exchanges:
            self.sync_orderbook(market, e)

    def sync_balances(self):
        balances = self.global_balances()
        self.logger.info("insert %s"%balances)
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
            self.logger.info("global orderbook %s %s"%(n,market))
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
                self.logger.error("error global orderbook %s %s %s"%(e,market,err))
        [bids,asks,ts] = orderbooks.aggregate_book(books)
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
            self.logger.error("symbol not supported")

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

    def sync_candle_timeframe(self, market, exchange, timeframe):
        self.logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_timeframe(market, exchange, timeframe)
        n = exc.NAMES[exchange]
        [nom,denom] = models.market_parts(market)
        self.db.candles.insert({"exchange":n,"market":market,"nom":nom,"denom":denom,"candles":candles,"interval": timeframe})

    def sync_candle_daily(self, market, exchange):
        self.logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_timeframe(market, exchange,self.acafade.TIMEFRAME_DAILY)
        n = exc.NAMES[exchange]
        [nom,denom] = models.market_parts(market)
        self.db.candles.insert({"exchange":n, "market":market, "nom":nom, "denom":denom, "candles":candles, "interval": "1d"})

    def sync_candle_minute(self, market, exchange):
        self.logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_timeframe(market, exchange,self.acafade.TIMEFRAME_1MINUTE)
        n = exc.NAMES[exchange]
        [nom,denom] = models.market_parts(market)
        dt = datetime.datetime.utcnow()
        dts = dt.strftime('%H:%M:%S')
        self.db.candles.insert({"exchange":n, "market":market, "nom":nom, "denom":denom, "candles":candles, "interval": "1m", "time_insert":dts})

    def sync_candle_minute15(self, market, exchange):
        self.logger.debug("get candles %s %s "%(market, str(exchange)))
        candles = self.afacade.get_candles_timeframe(market, exchange,self.acafade.TIMEFRAME_15MINUTE)
        n = exc.NAMES[exchange]
        [nom,denom] = models.market_parts(market)
        dt = datetime.datetime.utcnow()
        dts = dt.strftime('%H:%M:%S')
        self.db.candles.insert({"exchange":n, "market":market, "nom":nom, "denom":denom, "candles":candles, "interval": "1m", "time_insert":dts})

    def sync_candles_all(self, market):
        for e in self.active_exchanges:
            self.sync_candle_daily(market, e)

    def sync_candle_daily_all(self):
        ms = self.fetch_global_markets()
        self.logger.info(len(ms))

        #cndl = self.afacade.get_candles_daily(market,exc.BINANCE)

        for x in ms[:]:
            market = x['pair']
            self.logger.info("sync %s"%market)
            try:
                self.sync_candle_daily(market,exc.BINANCE)
            except:
                pass

    def sync_book_work(self, market, exchange):
        while True:
            self.sync_orderbook(market, exchange)
            time.sleep(10)

    def sync_book_thread(self, market, exchange):
        start_new_thread(self.sync_book_work(market, exchange))

    def transaction_queue(self,exchange):
        now = datetime.datetime.utcnow()
        #delta = now - self.starttime
        txs = self.afacade.get_tradehistory_all(exchange)
        for tx in txs[:]:
            ts = tx['timestamp'][:19]
            dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
            if dt > self.starttime:
                self.logger.info("new tx")
