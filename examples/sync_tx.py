"""

"""

import archon.facade as facade
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.model.models as models
from archon.util import *
from pymongo import MongoClient

import time
import datetime
import math


afacade = facade.Facade()
arch.setClientsFromFile(afacade)

a = arch.Arch()
ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA]
a.set_active_exchanges(ae)

if __name__=='__main__':
    nom = "LTC"
    denom = "BTC"
    market = models.market_from(nom, denom)
    a.sync_tx_all(market)

    db = a.get_db()
    for e in ae:
        n = exc.NAMES[e]
        txs = db.txs.find_one({'market':market,'exchange':n})
        print ("> ",txs['tx'][-1])