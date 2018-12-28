from archon.ws.bitmex.bitmex_ws import BitMEXWebsocket
import logging
from logging.handlers import RotatingFileHandler
from time import sleep
import datetime
import json
import toml

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
    logger = setup_logger()

    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1",
                         symbol=crypto, api_key=k, api_secret=s)
    logger.info("Instrument data: %s" % ws.get_instrument())
    logger.info("\n\n\n\n************\n\n\n")
    while(ws.ws.sock.connected):        
        logger.info("Ticker: %s" % ws.get_ticker())

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

        sleep(sleeping)

def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    # Change this to DEBUG if you want a lot more info
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = RotatingFileHandler(
        '_activity.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":
    
    filename = "apikeys.toml"
    apikeys = parse_toml(filename)['BITMEX']
    k,s = apikeys['public_key'],apikeys['secret']
    run(k,s)

