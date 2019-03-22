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

    def store_apikey(self, exchange, pubkey, secret, user_id=""):
        #check if exchange exists
        keys = {"exchange": exchange, "public_key": pubkey, "secret": secret}
        #self.db.apikeys.drop()
        self.db.apikeys.update_one({"user_id": user_id, "exchange": exchange}, {"$set": {"apikeys": keys}}, upsert=True)

        print (list(self.db.apikeys.find()))


    def get_apikeys(self, user_id=""):
        return list(self.db.apikeys.find({"user_id": user_id}))
        

    def activate_session(self, user_id):
        self.session_user_id = user_id
        self.session_active = True
        self.clients[user_id] = {}
    
    def set_client(self, exchange):
        """ set clients from stored keys """
        #self.logger.info ("set keys %s %s"%(exchange,keys['public_key']))
        if not self.session_active:
            raise Exception("no active session")

        self.logger.info("set api " + str(exchange))
        #keys = self.db.apikeys.find_one({"exchange":exchange})
        keys = self.db.apikeys.find_one({"user_id":self.session_user_id})["apikeys"]
        print ("?? ", keys)
        
        print (self.clients)
        if exchange==exc.BITMEX:            
            self.clients[self.session_user_id][exchange] = bitmex.BitMEX(apiKey=keys["public_key"], apiSecret=keys["secret"])
        elif exchange==exc.DELTA:
            self.clients[self.session_user_id][exchange] = DeltaRestClient(api_key=keys["public_key"], api_secret=keys["secret"])
            self.logger.debug("set %s"%exchange)

    def get_client(self, exchange):
        if not self.session_active:
            raise Exception("no active session")

        return self.clients[self.session_user_id][exchange]

