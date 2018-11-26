"""

"""

import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.model.models as model
from archon.util import *

import time
import datetime
import math

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC,exc.KRAKEN]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()


def show_book_exc(exchange, market):
    global a
    i = 0
    [bids,asks] = a.abroker.get_orderbook(market,exchange)
    name= exc.NAMES[exchange]
    print ("** bid **       %s     ** ask **"%(name))
    for b in bids[:10]:
        ask = asks[i]  
        bp = b['price']
        ap = ask['price']
        av = ask['quantity']
        bv = b['quantity']
        print ("%.8f  %.2f   %.8f  %.2f" % (bp,bv,ap,av))
        i+=1  

def show_book(nom,denom):
    #for e in [exc.CRYPTOPIA, exc.BITTREX, exc.KUCOIN]:
    for e in [exc.KRAKEN]:
        market = model.market_from(nom,denom)
        show_book_exc(e,market)

if __name__=='__main__':
    show_book("BTC","USD")
    show_book("BTC","EUR")
        