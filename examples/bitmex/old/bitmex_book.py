
import logging
import os
import time

import numpy
from pymongo import MongoClient
import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as m
import archon.exchange.bitmex.book_util as book_util


abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

def mid_price(book):
    """ ratio of top bid to top ask """
    bids,asks = book['bids'],book['asks']
    #asks.reverse()
    level = 0
    bp = bids[level]['price']
    ap = asks[level]['price']
    mid = (bp+ap)/2
    return mid

def get_book():
    market = m.market_from("XBT","USD")   
    smarket = m.conv_markets_to(market, exc.BITMEX) 
    book = abroker.afacade.get_orderbook(smarket, exc.BITMEX)
    return book

def show():    
    book = get_book()
    mid = mid_price(book)
    book_util.display_book(book)
    print ("mid price ",mid)

if __name__=='__main__':
    show()
