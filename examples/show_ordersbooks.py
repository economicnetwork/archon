"""

"""

import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.markets as m
import archon.model as model
from archon.util import *

import time
import datetime
import math

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

def show_book(exchange, market):
    i = 0    
    [bids,asks] = abroker.get_orderbook(market,exchange)
    name= exc.NAMES[exchange]
    print ("** bid **       %s     ** ask **"%(name))
    for b in bids[:10]:
        a = asks[i]  
        bp = b['price']
        ap = a['price']
        av = a['quantity']
        bv = b['quantity']
        print ("%.8f  %.0f   %.8f  %.0f" % (bp,bv,ap,av))
        i+=1  

if __name__=='__main__':
    nom = "LTC"
    denom = "BTC"
    for e in [exc.CRYPTOPIA, exc.BITTREX, exc.KUCOIN]:
        market = m.get_market(nom,denom,e)
        show_book(e,market)
        