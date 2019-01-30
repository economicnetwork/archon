"""
feeder. polls exchanges and publishes
"""

from datetime import datetime

import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
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


class Feeder(threading.Thread):
    
    def __init__(self, abroker):
        threading.Thread.__init__(self)
        setup_logger(logger_name="Feeder", log_file='feeder.log')
        self.log = logging.getLogger("Feeder")
        self.abroker = abroker
        self.log.info("init feeder")
        #r = redis.Redis(host='localhost', port=6379, db=0)
        self.redisclient = redis.StrictRedis(host='localhost', port=6379)  

        mex_sym = mex.instrument_btc_perp
        self.mex_sym = mex_sym

    def get_book(self):        
        book = self.abroker.afacade.get_orderbook(self.mex_sym, exc.BITMEX)
        return book

    def mex_position(self):
        mex_client = self.abroker.afacade.get_client(exc.BITMEX)
        pos = mex_client.position()
        return pos        

    def open_orders(self, e):
        if e==exc.BITMEX:
            oo = self.abroker.afacade.open_orders(exc.BITMEX)
            return oo     

    def pub_set(self, topic, data):
        """ publish and set """        
        #self.redisclient.publish(SUB_TOPIC_MARKET_BOOK_BITMEX, json.dumps({"topic":SUB_TOPIC_MARKET_BOOK_BITMEX,"data":book}))
        jdata = json.dumps({"topic":topic,"data":data})
        self.redisclient.publish(topic, jdata)
        t = rep + topic[4:]
        self.redisclient.set(t, data)

    def run(self):
        while True:
            print ("feeder loop")
            #TODO openorders
            #TODO position

            data = self.mex_position()
            print ("pos ",data)
            if data == []: data = "No position"
            
            self.pub_set(SUB_TOPIC_POS_BITMEX, data)

            oo = self.open_orders(exc.BITMEX)
            self.pub_set(SUB_TOPIC_ORDERS_BITMEX, oo)

            #self.redisclient.publish(SUB_TOPIC_ORDERS_BITMEX, json.dumps({"topic":SUB_TOPIC_ORDERS_BITMEX,"data":oo}))
            book = self.get_book()            
            self.pub_set(SUB_TOPIC_MARKET_BOOK_BITMEX, book)

            #book_util.display_book(self.book)

            time.sleep(5)
