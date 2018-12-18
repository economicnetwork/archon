"""

"""

import archon.facade as facade
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.model.models as m
from archon.util import *

import time
import datetime
import math

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def show(exchange, market):
    i = 0    
    txs = a.afacade.market_history(market,e)
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
        