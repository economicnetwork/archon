"""
show orderbooks for all exchanges
"""

import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as model
from archon.util import *

import time
import datetime
import math

abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file(exchanges=[exc.KRAKEN])

def display_book(book,name):
    [bids,asks] = book
    print ("** bid **       %s     ** ask **"%(name))
    i = 0
    for b in bids[:10]:
        ask = asks[i]  
        bp = b['price']
        ap = ask['price']
        av = ask['quantity']
        bv = b['quantity']
        print ("%.8f  %.2f   %.8f  %.2f" % (bp,bv,ap,av))
        i+=1  

def show_book_exc(exchange, market):
    global a
    smarket = model.conv_markets_to(market, exchange)   
    book = abroker.afacade.get_orderbook(smarket,exchange)
    name = exc.NAMES[exchange]
    display_book(book, name)

def show_book(nom,denom):
    for e in [exc.KRAKEN]:
        market = model.market_from(nom,denom)
        show_book_exc(e,market)

if __name__=='__main__':
    #show_book("LTC","BTC")
    show_book("BTC","USD")
    