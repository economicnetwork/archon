"""
basic strategy WIP
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

    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID = "mm-strategy1"
        #self.name = name
        #self.counter = counter
        config = agent_config()["AGENT"]
        m = config["market"]    
        self.agent_id = config["agentid"]
        self.abroker = broker.Broker()
        self.arch = arch.Arch()
        arch.setClientsFromFile(self.abroker)        
        nom,denom = m.split('_')
        self.e = exc.KUCOIN
        self.market = models.get_market(nom,denom,self.e)
        self.rho = config["rho"]

        self.openorders = list()

    def cancel_all(self):
        oo = self.abroker.open_orders_symbol(self.market,self.e)
        for o in oo:
            print ("cancelling ",o)
            result = self.abroker.cancel(o, exchange=self.e)
            print ("result" + str(result))


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
        print ("submit ",o)
        r = self.abroker.submit_order(o, self.e)
        print (r)

    def submit_sell(self,price, qty):
        o = [self.market, "SELL", price, qty]
        print ("submit ",o)
        r = self.abroker.submit_order(o, self.e)
        print (r)        

    def orderbook(self):
        [obids,oasks] = self.abroker.get_orderbook(self.market,self.e)
        return [obids,oasks]

    def submit_bid(self):
        pip = 0.0000001
        round_precision = 7
        [obids,oasks] = self.orderbook()
        
        bestbid = obids[0]['price']
        bestask = oasks[0]['price']
        spread = (bestask-bestbid)/bestask
        mid = (bestask+bestbid)/2
        print (bestbid,bestask,spread,mid)    
        rho = self.rho
        price_target = round(bestask*(1-rho),7)
        qty = 100
        self.submit_buy(price_target, qty)

    def submit_ask(self):
        pip = 0.0000001
        round_precision = 7
        [obids,oasks] = self.orderbook()
        
        bestbid = obids[0]['price']
        bestask = oasks[0]['price']
        spread = (bestask-bestbid)/bestask
        mid = (bestask+bestbid)/2
        rho = 0.0015
        price_target = round(mid*(1+rho),7)
        qty = 100
        self.submit_sell(price_target, qty)        

    def show_ob(self):
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
            self.openorders = self.abroker.open_orders_symbol(self.market,self.e)
            self.open_bids = list(filter(lambda x: x['otype']=='bid',self.openorders))
            self.open_asks = list(filter(lambda x: x['otype']=='ask',self.openorders))
        except:
            pass

    def run(self):
        print ("starting strategy")
        self.cancel_all()        
        while True:
            self.sync_openorders()
            print ('******')
                    
            print ("open orders ",self.openorders)
            print ("bids %i  asks %i"%(len(self.open_bids), len(self.open_asks)))

            [obids,oasks] = self.orderbook()
            self.show_stats([obids,oasks])

            if len(self.openorders) > 0:
                mybidprice = self.open_bids[0]['price']                
                bestbid = obids[0]['price']
                bestask = oasks[0]['price']
                self.show_ob()            

            else:
                print ("no open orders")
                #submit only once
                self.submit_bid()
                self.submit_ask()
            

            #self.arch.transaction_queue(self.e)
            time.sleep(10)

        #cancel_bids()
         

                
if __name__=='__main__':    
    strategy = Agent()
    strategy.start()
    strategy.join()
        