import datetime
import time
from pymongo import MongoClient
import pymongo
import logging
from loguru import logger

from archon.config import *
import archon.facade as facade
import archon.exchange.exchanges as exc
from archon.model import models
import archon.orderbooks as orderbooks
from archon.feeds import cryptocompare
from archon.util import *
import archon.model.models as m

import threading
from _thread import start_new_thread

def get_book(abroker):    
    symbol = "XBTUSD" 
    client = abroker.afacade.get_client(exc.BITMEX)   
    inst = client.get_instrument(symbol)
    print (inst['bidPrice'])
    print (inst['askPrice'])

    book = client.market_depth(symbol,depth=3)
    sells = list(filter(lambda x: x['side']=='Sell',book))
    buys = list(filter(lambda x: x['side']=='Buy',book))
    d = {'bids': buys, 'asks': sells}
    return d

def display_book(book,name):
    [bids,asks] = book
    print ("** bid **       %s     ** ask **"%(name))
    i = 0
    for b in bids[:10]:
        ask = asks[i]  
        bp = b['price']
        ap = ask['price']
        av = ask['quantity']
        bv = b['quantity']
        print ("%.8f  %.2f   %.8f  %.2f" % (bp,bv,ap,av))
        i+=1  

class SyncThread(object):
    
    def __init__(self, broker, interval=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.broker = broker
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ run worker """
    
        db = self.broker.get_db()
        col = db['bitmex_orderbook']

        i = 0    
        while i < 10:
            market = m.market_from("XBT","USD")
            book = self.broker.afacade.get_orderbook(market, exc.BITMEX)
            #book = get_book(self.broker)
            print (book)
            #db = abroker.get_db()
            col.insert_one(book)
            #x = list(db.orderbooks_history.find({}))
            #print (len(x))
            
            time.sleep(10)
            i+=1

        """    
        while True:
            print('sync orderbook in the background')
            market = models.market_from("XBT","USD")

            self.broker.sync_orderbook(market, exc.BITMEX)

            time.sleep(self.interval)
        """