"""
example how to get candles from N exchanges
"""
import sys
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.model.models as models

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
es = [exc.KUCOIN,exc.CRYPTOPIA,exc.BITTREX,exc.HITBTC]

def history(e):
    market = "LTC_BTC"
    n = exc.NAMES[e]
    print (n)    
    candles = abroker.get_candles_daily(market, e)    
    for x in candles[-5:]:
        print (x)
        

for e in es:
    history(e)
    