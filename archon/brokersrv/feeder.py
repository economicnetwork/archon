"""
feeder. polls exchanges and publishes
"""

from datetime import datetime

import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.exchange.deribit.Wrapper as deri
import archon.facade as facade
import archon.model.models as models
from archon.custom_logger import setup_logger, remove_loggers

from archon.util import *   

import pandas as pd
import numpy

import time
import json
import atexit
import logging
import threading
import time
import redis
from .topics import *


#default_symbols = {exc.BITMEX:mex.instrument_btc_perp}

class Feeder(threading.Thread):
    
    def __init__(self, abroker):
        threading.Thread.__init__(self)
        setup_logger(logger_name="Feeder", log_file='feeder.log')
        self.log = logging.getLogger("Feeder")
        self.abroker = abroker
        self.log.info("init feeder")
        self.redisclient = redis.StrictRedis(host='localhost', port=6379)  

        #TODO in config
        mex_sym = mex.instrument_btc_perp
        self.mex_sym = mex_sym


    def pub_set(self, topic, data):
        """ publish and set """        
        d = {"topic":topic,"data":data}
        jdata = json.dumps(d)
        self.redisclient.publish(topic, jdata)
        t = rep + topic[4:]
        self.redisclient.set(t, jdata)

        db = self.abroker.get_db()
        tt = topic[4:]
        #store
        db[tt].insert_one(d)

    def publish_bitmex(self):
        wait = 0.1 # bitmex rate limit 300 per 300 seconds
        pos = self.abroker.afacade.position(exc.BITMEX)
        pos = {"position": pos}
        time.sleep(wait)
        #print ("pos ",data)
        #print ("position ",pos)
        #if pos == []: pos = {}
        
        self.pub_set(SUB_TOPIC_POS_BITMEX, pos)

        oo = self.abroker.afacade.openorders(exc.BITMEX, mex.instrument_btc_perp)
        time.sleep(wait)
        self.pub_set(SUB_TOPIC_ORDERS_BITMEX, oo)

        book = self.abroker.afacade.orderbook(self.mex_sym, exc.BITMEX) 
        time.sleep(wait)
        self.pub_set(SUB_TOPIC_MARKET_BOOK_BITMEX, book)

    def publish_deribit(self):
        pos = self.abroker.afacade.position(exc.DERIBIT)
        if pos == None or pos == []: pos = {}
        self.pub_set(SUB_TOPIC_POS_DERIBIT, pos)

        oo = self.abroker.afacade.openorders(exc.DERIBIT, deri.instrument_btc_perp)
        if oo == None or oo == []: oo = {}
        self.pub_set(SUB_TOPIC_ORDERS_DERIBIT, oo)
        data = self.abroker.afacade.orderbook(deri.instrument_btc_perp, exc.DERIBIT) 
        self.pub_set(SUB_TOPIC_MARKET_BOOK_DERIBIT, data)


    def run(self):
        while True:
            self.log.info("feeder loop")
            #TODO openorders
            #TODO position

            self.publish_bitmex()
            self.publish_deribit()

            time.sleep(0.5)
