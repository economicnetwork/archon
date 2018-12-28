"""
broker only through websockets
"""

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

    def __init__(self):

        logger.start("log/broker.log", rotation="500 MB")

        logger.debug("init broker")

        self.afacade = facade.Facade()
        self.active_exchanges = list()
        self.selected_exchange = None
        self.set_keys_exchange_file()

        try:
            all_conf = parse_toml("conf.toml")

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
