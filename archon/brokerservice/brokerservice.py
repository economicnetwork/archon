"""
broker service
* is used by an external webapp
* user data is stored in the external webapp
* external process will register call back to get user_data
* broker stores all exchange relevant data: balances, orders, ...
"""

import datetime
import time
import logging
import os
import redis

from pathlib import Path
from pymongo import MongoClient

import archon.broker.facade as facade
import archon.exchange.exchanges as exc
import archon.util.orderbooks as orderbooks
from archon.broker.config import parse_toml
from archon.model import models
from archon.util.custom_logger import setup_logger
from archon.exchange.delta.delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size
from archon.exchange.bitmex import bitmex
from archon.exchange.kraken import KrakenAPI
import archon.exchange.binance as binance


class Brokerservice:

    def __init__(self, setMongo=True):

        setup_logger(logger_name="broker", log_file='broker.log')
        self.logger = logging.getLogger("broker")

        setMongo = True
        setRedis = True

        try:
            wdir = self.get_workingdir()
            path_file_config = wdir + "/" + "config.toml"
            config_dict = parse_toml(path_file_config)
        except:
                self.logger.error("no file. path expected: %s"%str(path_file_config))

        if setMongo:            
            try:
                mongo_conf = config_dict["MONGO"]
                uri = mongo_conf["uri"]
                self.set_mongo(uri)
                self.using_mongo = True
            except:
                self.using_mongo = False
                self.logger.error("could not set mongo")

            
        self.clients = {}

        self.starttime = datetime.datetime.utcnow()
        
        self.session_user_id = None
        self.session_active = False
                
        if setRedis:
            self.logger.info(config_dict)
            try:
                redis_conf = config_dict["REDIS"]       
                host = redis_conf["host"]     
                port = redis_conf["port"]
                self.redis_client = redis.Redis(host=host, port=port)
            except Exception as e:
                self.logger.error("could not set redis %s %s"%(str(host),str(port)))
                self.logger.error(str(e))

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

    def drop_apikey(self, exchange, user_id=""):
        self.db.apikeys.remove({"user_id": user_id, "exchange": exchange})

    def set_apikeys_fromfile(self, user_id=""):
        #store_apikey
        try:
            wdir = self.get_workingdir()
            api_file = wdir + "/" + "apikeys.toml"
            api_keys = parse_toml(api_file)
            #print (api_keys)
            self.db.apikeys.drop()
            for k,v in api_keys.items():
                self.store_apikey(k, v["public_key"], v["secret"], user_id)
                #pass
        except:
            self.logger.error("no file. path expected: %s"%str(api_file))

        #print ("apikeys ", list(self.db.apikeys.find()))

    def store_apikey(self, exchange, pubkey, secret, user_id=""):
        print ("store_apikey ", pubkey, " ", exchange)
        #check if exchange exists
        keys = {"exchange": exchange, "public_key": pubkey, "secret": secret}
        self.db.apikeys.update_one({"user_id": user_id, "exchange": exchange}, {"$set": {"apikeys": keys}}, upsert=True)
    

    def get_apikeys(self, user_id=""):
        return list(self.db.apikeys.find({"user_id": user_id}))
        
    def activate_session(self, user_id):
        print ("activate_session")
        self.session_user_id = user_id
        self.session_active = True
        print ("user_id ", user_id)
        print ("session_active ", self.session_active)
        self.clients[user_id] = {}
    
    def set_client(self, exchange):
        """ set clients from stored keys """
        #self.logger.info ("set keys %s %s"%(exchange,keys['public_key']))
        if not self.session_active:
            raise Exception("no active session")

        #keys = self.db.apikeys.find_one({"exchange":exchange})
        print ("set client ", self.session_user_id,  exchange)
        tmp = self.db.apikeys.find_one({"user_id":self.session_user_id, "exchange": exchange})
        print ("keys ", tmp)
        keys = tmp["apikeys"]
        self.logger.info("set api %s %s" %(str(exchange), keys["public_key"]))
        
        print ("clients ",self.clients)
        if exchange==exc.BITMEX:            
            print ("set bitmex")
            self.clients[self.session_user_id][exchange] = bitmex.BitMEX(apiKey=keys["public_key"], apiSecret=keys["secret"])
        elif exchange==exc.DELTA:
            self.clients[self.session_user_id][exchange] = DeltaRestClient(api_key=keys["public_key"], api_secret=keys["secret"])
            self.logger.debug("set %s"%exchange)
        elif exchange==exc.KRAKEN:
            self.clients[self.session_user_id][exchange] = KrakenAPI(keys["public_key"], keys["secret"])
        elif exchange==exc.BINANCE:
            self.clients[self.session_user_id][exchange] = binance.Client(keys["public_key"], keys["secret"])



    def get_client(self, exchange):
        if not self.session_active:
            raise Exception("no active session")

        #print (self.clients)
        return self.clients[self.session_user_id][exchange]

    # ----------------------------------

    def get_open_orders(self, exchange):
        client = self.clients[self.session_user_id][exchange]
        if exchange==exc.DELTA:
            oo = client.get_orders()
            return oo

    def get_position(self, exchange, product_id):
        client = self.clients[self.session_user_id][exchange]
        if exchange==exc.DELTA:
            pos = client.get_position(product_id)
            return pos

    def get_tx(self, exchange):
        client = self.clients[self.session_user_id][exchange]
        if exchange==exc.DELTA:
            fills = client.fills()
            return fills

    def get_orderbook(self, product_id, exchange):
        client = self.clients[self.session_user_id][exchange]

        if exchange==exc.DELTA:
            book = client.get_L2_orders(product_id)
            return book

        elif exchange==exc.BITMEX:
            bookdepth = 10
            ob = client.market_depth(product_id,depth=bookdepth)
            book = models.conv_orderbook(ob, exchange)
            return book


    def get_orders_bitmex(self):
        client = self.clients[self.session_user_id][exc.BITMEX]
        #TODO
        sym = bitmex.instrument_btc_mar19
        return client.open_orders(sym)

    # ---- global data ----
    
    def all_get_orders(self):
        ood = self.get_open_orders(exc.DELTA)
        #oob = self.get_open_orders(exc.BITMEX)
        #TODO
        oob = self.get_orders_bitmex()
        #oob = get_orders_bitmex()

        oo = {exc.DELTA: ood, exc.BITMEX: oob}
        return oo


    def get_btc_balances(self):
        bitmex_client = self.clients[self.session_user_id][exc.BITMEX]
        delta_client = self.clients[self.session_user_id][exc.DELTA]
        mex_funds = bitmex_client.funds()
        sat = 100000000
        mex_btc_balance = mex_funds["amount"]/sat

        DELTA_ASSET_BTC = 2        
        delta_btc_balance = float(delta_client.get_wallet(DELTA_ASSET_BTC)["balance"])

        total_balance = mex_btc_balance + delta_btc_balance
        
        funds = [{exc.BITMEX: {"BTC_balance": mex_btc_balance}, exc.DELTA: {"BTC_balance": delta_btc_balance}, "total": total_balance}]
        #funds = {exc.BITMEX: mex_funds, exc.DELTA: }
        return funds

    def get_tx_delta(self):
        delta_client = self.clients[self.session_user_id][exc.DELTA]
        t = delta_client.trade_history()
        now = datetime.datetime.now()
        tv = 0
        tx = list()
        for x in t[:]:
            ot, size, side, ap, crm, state = x['order_type'], x['size'], x['side'], x["avg_fill_price"], x["created_at"], x["state"]
            date = crm[:10]
            day = int(date[-2:])
            #if (day == now.day) and state != "cancelled":
            if state != "cancelled":
                try:
                    tv += float(size)
                    tx.append({"exchange": exc.DELTA, "type": ot, "size": size, "side": side, "avg_fill_price": ap, "state": state, "date": crm})
                except:
                    continue
        return tx

    def get_tx_all(self):
        bitmex_client = self.clients[self.session_user_id][exc.BITMEX]
        delta_client = self.clients[self.session_user_id][exc.DELTA]
        sym = bitmex.instrument_btc_mar19
        tx_bitmex = bitmex_client.execution_history_all(sym)
        tx_delta = self.get_tx_delta()
        tx_all = {exc.BITMEX: tx_bitmex, exc.DELTA: tx_delta}
        return tx_all


        

