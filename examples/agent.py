"""
basic strategy
will submit a bid and ask only once

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

    def __init__(self, exchange, market):        
        threading.Thread.__init__(self)   
        self.exchange=exchange     
        #config = agent_config()["AGENT"]
        #m = config["market"]    
        self.agent_id = "strategy" #config["agentid"]
        self.threadID = "thread-" + self.agent_id
        self.abroker = broker.Broker()
        self.arch = arch.Arch()
        arch.setClientsFromFile(self.abroker)        
        nom,denom = market.split('_')
        
        self.market = models.get_market(nom,denom,self.exchange)
        self.rho = 0.03        
        self.openorders = list()
        self.round_precision = 8
        #pip paramter for ordering
        self.pip = 0.0000001

    def cancel_all(self):
        oo = self.abroker.open_orders_symbol(self.market,self.exchange)
        for o in oo:
            print ("cancelling ",o)
            result = self.abroker.cancel(o)
            print ("result" + str(result))


    def cancel_bids(self):
        oo = self.abroker.open_orders_symbol(self.market,self.exchange)
        n = exc.NAMES[self.exchange]
        i = 0
        for o in oo:
            if o['otype']=='bid':
                print ("cancelling ",o)
                k = "oid"
                oid = o[k]
                result = self.abroker.cancel(o)
                print ("result" + str(result))

    def submit_buy(self,price, qty):
        o = [self.market, "BUY", price, qty]
        print ("submit ",o)
        r = self.abroker.submit_order(o, self.exchange)
        print (r)

    def submit_sell(self,price, qty):
        o = [self.market, "SELL", price, qty]
        print ("submit ",o)
        r = self.abroker.submit_order(o, self.exchange)
        print (r)        

    def orderbook(self):
        [obids,oasks] = self.abroker.get_orderbook(self.market,self.exchange)
        return [obids,oasks]
    
    def show_ob(self):
        """ show orderbook """
        oo = self.abroker.open_orders_symbol(self.market,self.exchange)
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
                print (p,q,"*")
            else:
                print (p,q)
        print ('-----')        
        for b in obids[:5]:
            p,q = b['price'],b['quantity']
            if p == mybidprice:
                print (p,q,"*")
            else:
                print (p,q)

    def sync_openorders(self):
        try:
            self.openorders = self.abroker.open_orders_symbol(self.market,self.exchange)
            self.open_bids = list(filter(lambda x: x['otype']=='bid',self.openorders))
            self.open_asks = list(filter(lambda x: x['otype']=='ask',self.openorders))
        except:
            pass

    def run(self):
        raise NotImplementedError("error message")
