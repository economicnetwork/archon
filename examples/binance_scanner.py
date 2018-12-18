import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch
import json
import requests
import time
import datetime
import archon.candles as c

a = arch.Arch()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

ae = [exc.BINANCE]
a.set_active_exchanges(ae)

def analyse(p):
    #x = afacade.get_candles_hourly(p,exc.BINANCE)
    x = afacade.get_candles_daily(p,exc.BINANCE)
    candles = x[-10:]
    print (c.max_close(candles))
    for z in x[-10:]:
        ts = z[0]
        o,h,l,c = z[1:5]
        print (ts,c,z[5])
    




ms = a.fetch_global_markets()

ms = list(filter(lambda x: x['denom'] == 'BTC', ms))
print (len(ms))


for x in ms[:2]:
    print (x)
    p = x['pair']
    analyse(p)