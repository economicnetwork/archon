"""
basic candle based strategy
"""

import sys

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.model.models as models
from util import *

import json
import requests
import pickle
import time

from agent import Agent

import traceback
from loguru import logger

class BasicStrategy(Agent):

    def __init__(self, arch):
        super().__init__(arch)
        
    def show_balance(self):
        b = self.arch.abroker.balance_all(exc.BINANCE)
        btc_b = list(filter(lambda x: x["symbol"] == "BTC", b))[0]["amount"]
        
    def candle_signal(self, candles, market):
        down = 0
        prevc = -1
        firstprice = candles[0][4]
        lastprice = candles[-1][4]
        for z in candles[-10:]:
            ts = z[0]
            o,h,l,c = z[1:5]
            c = float(c)            
            prevc = c
            print (ts,c)

        if lastprice > firstprice:
            logger.info("%s %s %.5f %i"%(market,ts,c))
        

    def sync_all_candles(self, markets):
        for m in markets[:10]:
            try:
                s = m['nom']
                market = models.market_from(s,"BTC")
                self.arch.sync_candle_minute(market,exc.BINANCE)
                
                x = self.arch.db.candles.find_one()
                logger.info(x["time_insert"])
                time.sleep(0.05)
            except Exception as err:
                logger.error("pair error %s"%err) 

    def show_candles(self):
        allx = self.arch.db.candles.find()
        for x in allx:
            c = x['candles']
            self.candle_signal(c,x["market"])

    def run(self):
        logger.info("starting basic strategy")
        series = list()

        markets = self.arch.fetch_global_markets(denom='BTC')
        #self.show_balance()

        while True:
            
            try:
                self.sync_openorders()     
                oo = self.openorders                
                logger.info("open orders %s"%str(oo))

                self.arch.db.candles.drop()
                self.sync_all_candles(markets)

                if len(oo) > 0:
                    logger.info("cancel all")
                    #self.cancel_all()

                else:
                    logger.info("scan number of markets %i"%len(markets))

                    self.show_candles()
                    
            except Exception as err:
                #traceback.print_exc()
                logger.error("error %s"%err)

            time.sleep(5.0)


if __name__=='__main__':
    a = arch.Arch()
    a.set_keys_exchange_file()
    ae = [exc.BINANCE]
    a.set_active_exchanges(ae)
    #import pdb
    #pdb.set_trace()
    try:
        ag = BasicStrategy(a)
        ag.run()
        strat_started = True
    except Exception as err:
        print ("bot not started ",err)
