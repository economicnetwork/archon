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

def show(exchange, market):
    i = 0    
    txs = abroker.market_history(market,e)
    name= exc.NAMES[exchange]
    for tx in txs[:10]:
        print (tx)
        #print ("%.8f  %.0f   %.8f  %.0f" % (bp,bv,ap,av))
        

if __name__=='__main__':
    nom = "LTC"
    denom = "BTC"
    for e in [exc.CRYPTOPIA, exc.BITTREX, exc.KUCOIN]:
        market = m.get_market(nom,denom,e)
        show(e,market)
        