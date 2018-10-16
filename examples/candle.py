import sys
sys.path.append('/Users/ben/archon')

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.model.models as models

import pandas


abroker = broker.Broker()
arch.setClientsFromFile(abroker)
client = abroker.get_client(exc.KUCOIN)

es = [exc.KUCOIN,exc.CRYPTOPIA,exc.BITTREX]


def history(e):
    market = "LTC_BTC"
    print (e)
    
    candles = abroker.get_candles_daily(market, e)    
    for x in candles[-5:]:
        print (x)
        

for e in es:
    history(e)
    