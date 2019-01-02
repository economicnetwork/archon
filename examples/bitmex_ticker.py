from archon.ws.bitmex.bitmex_ws import BitMEXWebsocket
import logging
from logging.handlers import RotatingFileHandler
from time import sleep
import datetime
import json
import toml
from loguru import logger

crypto = "XBTUSD"


def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def parse_toml(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def run(k,s):
    
    logger.info("run")

    bitmexws = BitMEXWebsocket(symbol=crypto, api_key=k, api_secret=s)

    #logger.info("Instrument data: %s" % ws.get_instrument())
    logger.info("\n\n\n\n************\n\n\n")
    while(bitmexws.ws.sock.connected):        
        logger.info("Ticker: %s" % bitmexws.get_ticker())
        #logger.info("Open orders: %s" % bitmexws.open_orders(''))
        #t = bitmexws.recent_trades()
        #logger.info("recent trades: %i" % len(t))

        sleep(5.0)

if __name__ == "__main__":
    
    filename = "apikeys.toml"
    apikeys = parse_toml(filename)['BITMEX']
    k,s = apikeys['public_key'],apikeys['secret']
    run(k,s)

