from archon.ws.bitmex.bitmex_ws import BitMEXWebsocket
from archon.wsbroker import WSBroker

import logging
from logging.handlers import RotatingFileHandler
from time import sleep
import datetime
import json
import toml
import time
from loguru import logger


sleeping = 1


def print_orderbook(ob):
    print ('*** orderbook ***')
    bids = ob['bids']
    asks = ob['asks']
    COL_PRICE = 0
    COL_QTY = 1
    for i in range(10):
        b = bids[i]
        a = asks[i]
        bp,bq = b
        ap,aq = a
        print (bp," ",bq,"    ",ap," ",aq)
    
    top_bid = bids[0]
    top_ask = asks[0]
    top_bid_qty = top_bid[COL_QTY]
    top_ask_qty = top_ask[COL_QTY]
    print (top_bid_qty>top_ask_qty)
    

def run():

    wsbroker = WSBroker()
    #logger.info("Instrument data: %s" % ws.get_instrument())
    logger.info("\n\n\n\n************\n\n\n")
    time.sleep(1)
    while(wsbroker.bitmexws.ws.sock.connected):
        #logger.info("Ticker: %s" % ws.get_ticker())

        ob = wsbroker.bitmexws.market_depth()
        print_orderbook(ob)

        #margindata = bws.data['margin'][0]
        #print ("data ",margindata) #['walletBalance'])

        #positiondata = bws.data['position']
        #print (positiondata)
            
        time.sleep(10)

        


if __name__ == "__main__":
        run()
    
