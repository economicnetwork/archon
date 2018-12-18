"""
main eventloop (experimental)
"""

import sys
import os
import threading

import archon
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.markets as markets
import time
import datetime
import toml
import archon.model.models as models
from util import *

logpath = './log'
log = setup_logger(logpath, 'info_logger', 'mm')


class Eventloop(threading.Thread):

    def __init__(self, afacade):
        threading.Thread.__init__(self)        
        self.afacade = afacade
        self.last_published_minute = -1
        self.market = "DCR_BTC"
        #self.exchange = exc.BITTREX
        self.exchange = exc.BINANCE

    def emit_candle(self, now):
        print ("new minute")
        candles = self.afacade.get_candles_minute(self.market, self.exchange)
        print ("pub ",candles[-1])
        self.last_published_minute = now.minute

    def run(self):
        #setup
        log.debug("start loop")
        candles = self.afacade.get_candles_minute(self.market, self.exchange)
        print ("last candle ",candles[-1])
        while True:
            #log.info('loop')

            now = datetime.datetime.now()
            s = now.second
                        
            if s > 1 and s < 5:
                if now.minute > self.last_published_minute:
                    self.emit_candle(now)
                    
                else:
                    log.debug("already published")
            else:
                log.debug("wait for next minute")

            """
            ms = now.microsecond
            if ms < 100000:
                print ("second")
            """
            #check

            #broadcast

            time.sleep(0.1)


