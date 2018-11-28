"""
example how to get candles from N exchanges
"""
import sys
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.model.models as models

a = arch.Arch()
a.set_keys_exchange_file()
es = [exc.KUCOIN,exc.BITTREX]

def history(e):
    market = "DCR_BTC"
    n = exc.NAMES[e]
    print (n)    
    candles = a.abroker.get_candles_minute(market, e)    
    for x in candles[:]:
        print (x)
        

for e in es:
    history(e)
    