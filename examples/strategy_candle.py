"""
example candle based strategy
customized to binance currently
"""

import sys

import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch
import archon.model.models as models
from archon.agent import *

from util import *

import json
import requests
import pickle
import time


import traceback
from loguru import logger
import pdb


class Candletrategy(Agent):

    def __init__(self, arch):
        super().__init__(arch, exc.BINANCE)
        
    def show_balance(self,ETH_BTC,EOS_BTC):
        b = self.balances()
        btc_b = list(filter(lambda x: x["symbol"] == "BTC", b))[0]["amount"]
        logger.info("BTC %.5f"%btc_b)
        
    def showcandles(self, candles):    
        for z in candles[-10:]:
            ts,o,h,l,c = z[:5]
            c = float(c)
            logger.debug("%s %6.f"%(ts,c))


    def candle_signal(self, candles, market):
        """ signal returns action or no action """

        COL_CLOSE = 4
        start_price = float(candles[-10][COL_CLOSE])
        now_price = float(candles[-1][COL_CLOSE])
        ROC = now_price/start_price -1
        
        if ROC > 0.1:
            buy_signal = SIGNAL_LONG
        else: 
            buy_signal = SIGNAL_NOACTION

        logger.info("SIGNAL %i %s"%(buy_signal,market))                
            

    def buy(self, market):
        """ perform buy on binance. needs to be abstracted in broker """
        
        logger.debug("get ",market)

        logger.info("submit buy")

        [bids,asks] = self.orderbook(market)
        bid = float(bids[0]['price'])
        ask = float(asks[0]['price'])
        mid = (bid + ask)/2

        #TODO binance conversion needs to be pushed to broker
        btc_qty = 0.05
        qty_target = round(btc_qty/mid,0)
        qty_target = f'{qty_target:.6f}'
        rho = 0.005
        price_target = round(mid * (1 + rho),6)
        price_target = f'{price_target:.6f}'
        o = [market, "BUY", price_target, qty_target]
        logger.info ("order %s" % str(o))
        r = self.arch.afacade.submit_order(o,exc.BINANCE)
        logger.info("submit result "%r)
        
    def sync_all_candles(self, markets):
        logger.debug("sync candles for %i markets"%(len(markets)))
        for m in markets[:50]:
            try:
                s = m['nom']
                market = models.market_from(s,"BTC")
                #candles = self.afacade.get_candles_minute(market,exc.BINANCE)
                self.arch.sync_candle_minute15(market,exc.BINANCE)
                
                x = self.arch.db.candles.find_one()
                logger.debug(x["time_insert"])
                #self.candle_signal(candles, market)
                #self.checkpair(market)
                time.sleep(0.05)
            except Exception as err:
                logger.error("pair error %s"%err) 

    def check_signal(self):
        allx = self.arch.db.candles.find()
        for x in allx:
            c = x['candles']
            m = x["market"]
            logger.info("check signal %s"%m)
            signal = self.candle_signal(c,m)
            if signal == SIGNAL_LONG:
                logger.info("BUY ",m)
                self.buy(m)
            else:
                logger.info("no signal ",m)

    def run(self):
        logger.info("starting example strategy")
        series = list()

        markets = self.arch.fetch_global_markets(denom='BTC')
        logger.info("market founds %i"%(len(markets)))
        for m in markets: logger.debug("market found %s"%str(m))

        while True:
            #loop every X minutes. this can be pushed to event emitter, but keep in thread for now
            minute = 60.0
            timesleep = 15 * minute        

            b = self.arch.afacade.balance_all(exc.BINANCE)
            logger.info(b)
            
            try:
                self.sync_openorders()     
                oo = self.openorders                
                logger.info("open orders %s"%str(oo))

                self.arch.db.candles.drop()
                self.sync_all_candles(markets)

                if len(oo) > 0:
                    logger.info("open orders. cancel all")
                    #self.cancel_all()

                else:
                    logger.info("scan number of markets %i"%len(markets))

                    self.check_signal()
                    
            except Exception as error:
                logger.error("error %s"%error)
                logging.fatal(error, exc_info=True)
            
            time.sleep(timesleep)


if __name__=='__main__':
    #only binance currently
    a = arch.Arch()
    a.set_keys_exchange_file()
    ae = [exc.BINANCE]
    a.set_active_exchanges(ae)
    try:
        ag = Candletrategy(a)
        ag.run()
        strat_started = True
    except Exception as err:
        print ("bot not started ",err)
