import datetime
import time
from pymongo import MongoClient
import logging
from loguru import logger

from archon.config import *
import archon.facade as facade
import archon.exchange.exchanges as exc
from archon.model import models
import archon.orderbooks as orderbooks
from archon.feeds import cryptocompare
from archon.util import *
from archon.ws.bitmex.bitmex_ws import BitMEXWebsocket


class WSBroker:
    """ 
    WS version, currenlty only bitmex
    communicate with exchanges via facade
    keeps datastructures in memory
    """

    def __init__(self):

        logger.start("log/wsbroker.log", rotation="500 MB")
        logger.debug("init ws broker")

        filename = "apikeys.toml"
        apikeys = parse_toml(filename)['BITMEX']
        k,s = apikeys['public_key'],apikeys['secret']
        symbol = "XBTUSD"
        self.bitmexws = BitMEXWebsocket(symbol=symbol, api_key=k, api_secret=s)
        #run(k,s)

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

        #workaround for urllib logger verbosity
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        
    def set_mongo(self, url, dbName):
        self.mongo_url = url
        logger.debug("using mongo " + str(url))
        self.mongoclient = MongoClient(self.mongo_url)
        logger.debug("db %s"%dbName)
        self.db = self.mongoclient[dbName]

    def get_db(self):
        return self.db

    
