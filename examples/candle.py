"""
example how to get candles from N exchanges
"""
import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker
import archon.model.models as models

a = broker.Broker()
a.set_keys_exchange_file()
es = [exc.KUCOIN,exc.CRYPTOPIA,exc.BITTREX,exc.HITBTC]

def history(e):
    market = "LTC_BTC"
    n = exc.NAMES[e]
    print (n)    
    candles = a.afacade.get_candles_daily(market, e)    
    for x in candles[-5:]:
        print (x)
        

for e in es:
    history(e)
    