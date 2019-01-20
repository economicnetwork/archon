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

from apscheduler.schedulers.blocking import BlockingScheduler
sched_logger = logging.getLogger("apscheduler") 
sched_logger.setLevel(logging.WARNING)

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

        #thread = threading.Thread(target=self.run, args=())
        #thread.daemon = True                            # Daemonize thread
        #thread.start()                                  # Start the execution

        scheduler = BlockingScheduler()
        scheduler.add_job(self.sync_job, 'interval', seconds=10)
        scheduler.start()

    def sync_job(self):
        """ run worker """
    
        db = self.broker.get_db()
        col = db.orderbooks #['bitmex_orderbook']

        #i = 0    
        logger.debug('sync in the background')
        #while True:
        market = m.market_from("XBT","USD")
        smarket = models.conv_markets_to(market, exc.BITMEX)  
        self.broker.sync_orderbook(smarket, exc.BITMEX)
        self.broker.sync_trades(smarket, exc.BITMEX)
            
            
            #col.insert_one(book)
            #logger.debug("sync.. %s"%str(book))
            #print (book)
            
        #time.sleep(5)
        #i+=1

        """            
            market = models.market_from("XBT","USD")
            self.broker.sync_orderbook(market, exc.BITMEX)        
        """

