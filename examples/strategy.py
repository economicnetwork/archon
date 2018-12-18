"""
basic strategy
will submit a bid and ask only once

"""

import sys
import os
import threading

import archon
import archon.facade as facade
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
from agent import Agent

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def agent_config():
    toml_string = toml_file("agent.toml")
    parsed_toml = toml.loads(toml_string)
    return parsed_toml


logpath = './log'
log = setup_logger(logpath, 'info_logger', 'mm')


class MyStrategy(Agent):

    def __init__(self):        
        e = exc.BITTREX
        market = "LTC_BTC"
        super().__init__(e, market)        

    def submit_bid(self): 
        """ submit bid strategy """               
        [obids,oasks] = self.orderbook()
        
        bestbid = obids[0]['price']
        bestask = oasks[0]['price']
        spread = (bestask-bestbid)/bestask
        mid = (bestask+bestbid)/2
        print (bestbid,bestask,spread,mid)    
        rho = 0.1
        price_target = round(bestask*(1-rho),self.round_precision)
        qty = round(0.05/mid,self.round_precision)
        print ("submit ", price_target, " ",qty)
        self.submit_buy(price_target, qty)

    def submit_ask(self):
        [obids,oasks] = self.orderbook()
        
        bestbid = obids[0]['price']
        bestask = oasks[0]['price']
        spread = (bestask-bestbid)/bestask
        mid = (bestask+bestbid)/2
        rho = 0.1
        price_target = round(mid*(1+rho),self.round_precision)
        qty = 0.05/mid
        self.submit_sell(price_target, qty)   

    def run(self):
        print ("starting strategy")
        self.cancel_all()        
        while True:
            self.sync_openorders()
            print ('******')
                    
            print ("open orders ",self.openorders)
            print ("bids %i  asks %i"%(len(self.open_bids), len(self.open_asks)))

            [obids,oasks] = self.orderbook()

            if len(self.openorders) > 0:
                mybidprice = self.open_bids[0]['price']                
                bestbid = obids[0]['price']
                bestask = oasks[0]['price']
                self.show_ob()            

            else:
                print ("no open orders. submit bid once")
                #submit only once
                self.submit_bid()
                #self.submit_ask()

            #self.arch.transaction_queue(self.e)
            time.sleep(10)

        #cancel_bids()        
                
if __name__=='__main__':        
    strategy = MyStrategy()
    strategy.start()
    strategy.join()
        