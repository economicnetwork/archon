"""

"""

import archon.facade as facade
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.model.models as models
from archon.util import *

import time
import datetime
import math

afacade = facade.Facade()
arch.setClientsFromFile(afacade)

def show(exchange, market):
    i = 0    
    txs = afacade.market_history(market,e)
    name = exc.NAMES[exchange]
    for tx in txs[:10]:
        print (tx)
        #print ("%.8f  %.0f   %.8f  %.0f" % (bp,bv,ap,av))
        

if __name__=='__main__':
    nom = "LTC"
    denom = "BTC"
    for e in [exc.CRYPTOPIA, exc.BITTREX, exc.KUCOIN]:
        market = models.get_market(nom,denom,e)
        show(e,market)
        