"""
basic agent
"""

import sys
import os
import threading

import archon
import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.markets as markets
import time
import datetime
import toml
import archon.model.models as models

from util import *
import random
import math
from loguru import logger

SIGNAL_LONG = 1
SIGNAL_NOACTION = 0


def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def agent_config():
    toml_string = toml_file("agent.toml")
    parsed_toml = toml.loads(toml_string)
    return parsed_toml


logpath = './log'
log = setup_logger(logpath, 'info_logger', 'mm')


class Agent(threading.Thread):

    def __init__(self, arch, exchange):
        threading.Thread.__init__(self)        
        #config = agent_config()["AGENT"]
        #m = config["market"]    
        market = "LTC_BTC"
        self.agent_id = "agent" #config["agentid"]
        self.threadID = "thread-" + self.agent_id
        self.abroker = arch.abroker
        self.arch = arch
        nom,denom = market.split('_')
        #TODO config
        self.e = exchange
        #self.market = models.get_market(nom,denom,self.e)
        self.market = market
        self.rho = 0.1

        self.openorders = list()

        self.round_precision = 8
        #pip paramter for ordering
        self.pip = 0.0000001
        logger.info("agent inited")

    def balances(self):
        b = self.arch.abroker.balance_all(exc.BINANCE)
        return b

    def cancel_all(self):
        logger.info("cancel all")
        oo = self.openorders
        logger.info(oo)
        for o in oo:
            print ("cancelling ",o)
            result = self.abroker.cancel(o) #, exchange=self.e)
            print ("cancel result: " + str(result))
            time.sleep(0.5)


    def cancel_bids(self):
        oo = self.abroker.open_orders_symbol(self.market,self.e)
        n = exc.NAMES[self.e]
        i = 0
        for o in oo:
            if o['otype']=='bid':
                print ("cancelling ",o)
                k = "oid"
                oid = o[k]
                result = self.abroker.cancel(o, exchange=self.e)
                print ("result" + str(result))

    def submit_buy(self,price, qty):
        o = [self.market, "BUY", price, qty]
        logger.info("submit ",o)
        [order_result,order_success] = self.abroker.submit_order(o, self.e)
        logger.info(order_result,order_success)

    def submit_sell(self,price, qty):
        o = [self.market, "SELL", price, qty]
        logger.info("submit ",o)
        [order_result,order_success] = self.abroker.submit_order(o, self.e)
        logger.info(order_result,order_success)   

    def orderbook(self,market=None):        
        if market==None: market=self.market
        logger.debug("get orderbook %s"%market)
        [obids,oasks] = self.abroker.get_orderbook(market,self.e)
        return [obids,oasks]

    def global_orderbook(self,market=None):
        if market==None: market=self.market
        [obids,oasks,ts] = self.arch.get_global_orderbook(market)
        return [obids,oasks,ts]

    def show_ob(self):
        """ show orderbook """
        oo = self.abroker.open_orders_symbol(self.market,self.e)
        open_bids = list(filter(lambda x: x['otype']=='bid',oo))
        open_asks = list(filter(lambda x: x['otype']=='ask',oo))
        mybidprice = -1
        myaskprice = -1
        if len(open_bids)>0:
            mybidprice = open_bids[0]['price']
        if len(open_asks)>0:
            myaskprice = open_asks[0]['price']            

        else:
            mybidprice = 0
        [obids,oasks] = self.orderbook()
        
        #print (oo)
        oasks.reverse()
        for a in oasks[-3:]:
            p,q = a['price'],a['quantity']
            if p == myaskprice:
                logger.debug(p,q,"*")
            else:
                logger.debug(p,q)
        logger.debug('-----')        
        for b in obids[:5]:
            p,q = b['price'],b['quantity']
            if p == mybidprice:
                logger.debug(p,q,"*")
            else:
                logger.debug(p,q)

    def sync_openorders(self):
        try:
            log.info("sync orders " + str(self.e))
            #oo = self.abroker.open_orders_symbol(self.market,self.e)
            oo = self.abroker.open_orders(exc.BINANCE)
            log.info("oo " + str(oo))
            if oo != None:
                self.openorders = oo
                self.open_bids = list(filter(lambda x: x['otype']=='bid',self.openorders))
                self.open_asks = list(filter(lambda x: x['otype']=='ask',self.openorders))
        except Exception as e:
            logger.error(e)

    def run(self):
        raise NotImplementedError("error message")
