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

class Brokerservice:

    def __init__(self, setMongo=True):

        setup_logger(logger_name="broker", log_file='broker.log')
        self.logger = logging.getLogger("broker")

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

            
        self.clients = {}

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

    def drop_apikey(self, exchange, user_id=""):
        self.db.apikeys.remove({"user_id": user_id, "exchange": exchange})

    def store_apikey(self, exchange, pubkey, secret, user_id=""):
        #check if exchange exists
        #ping exchange?
        #upsert??
        #coll.update(key, data, upsert=True);
        #self.db.apikeys.update_one({"exchange": exchange, "pubkey": pubkey, "secret": secret, "user_id": user_id}, upsert=True)
        #self.db.apikeys.drop()
        if self.db.apikeys.find({"user_id": user_id, "exchange": exchange}).count()==0:
            self.db.apikeys.insert_one({"exchange": exchange, "pubkey": pubkey, "secret": secret, "user_id": user_id})
        #db.users.update_one({"_id" : string1.id, "name" : string1.name, "perm" : "administrator"}, upsert=False)

    def get_apikeys(self, user_id=""):
        return list(self.db.apikeys.find({"user_id": user_id}))
        
    def set_client(self, exchange, key, secret, user_id=""):
        """ set clients """
        #self.logger.info ("set keys %s %s"%(exchange,keys['public_key']))
        self.logger.info("set api " + str(exchange))
        if user_id not in self.clients.keys():
            self.clients[user_id] = {}
        if exchange==exc.BITMEX:
            self.clients[user_id][exchange] = bitmex.BitMEX(apiKey=key, apiSecret=secret)
        elif exchange==exc.DELTA:
            self.clients[user_id][exchange] = DeltaRestClient(api_key=key, api_secret=secret)
            self.logger.debug("set %s"%exchange)

    def get_client(self, user_id, exchange):
        return self.clients[user_id][exchange]

