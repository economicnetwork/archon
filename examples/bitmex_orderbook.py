from archon.ws.bitmex.bitmex_ws import BitMEXWebsocket
import logging
from logging.handlers import RotatingFileHandler
from time import sleep
import datetime
import json
import toml
import time
from loguru import logger

crypto = "XBTUSD"
sleeping = 1

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def parse_toml(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def run(k,s):

    bws = BitMEXWebsocket(symbol=crypto, api_key=k, api_secret=s)
    #logger.info("Instrument data: %s" % ws.get_instrument())
    logger.info("\n\n\n\n************\n\n\n")
    time.sleep(1)
    while(bws.ws.sock.connected):
        print ("loop")
        #logger.info("Ticker: %s" % ws.get_ticker())

        ob = bws.market_depth()
        print (ob)

        #margindata = bws.data['margin'][0]
        #print ("data ",margindata) #['walletBalance'])

        #positiondata = bws.data['position']
        #print (positiondata)
        time.sleep(10)

        """
        bids = ob['bids']
        asks = ob['asks']
        for i in range(10):
            b = bids[i]
            a = asks[i]
            print (b,a)
        
        """

        """      
        

        logger.info("Open orders: %s" % ws.open_orders(''))

        t = ws.recent_trades()
        logger.info("recent trades: %i" % len(t))

        d = ws.market_depth()
        logger.info("depth %i " % len(d))
        sells = list(filter(lambda d: d['side'] == 'Sell' , d))        
        buys = list(filter(lambda d: d['side'] == 'Buy' , d))        
        #sells = list(filter(lambda d: d['side'] == 'Sell' , d))        
        #logger.info(sells[0])
        topbuys = buys[:5]
        topsells = sells[-5:]
        #logger.info(buys[-1])
        logger.info("depth sells %i " % len(sells))
        logger.info("depth  buys %i " % len(buys))

        for i in range(5):
            bp,bq = topbuys[i]['price'],topbuys[i]['size']
            sp,sq = topsells[i]['price'],topsells[i]['size']
            logger.info("%5.3f   %5.2f"%(bp,sp))
        """

        


if __name__ == "__main__":
    
    filename = "apikeys.toml"
    apikeys = parse_toml(filename)['BITMEX']
    k,s = apikeys['public_key'],apikeys['secret']
    run(k,s)

