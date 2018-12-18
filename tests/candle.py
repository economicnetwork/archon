import sys
sys.path.append('/Users/ben/archon')

import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch
import archon.model.models as models

import pandas


afacade = facade.Facade()
arch.setClientsFromFile(afacade)
client = afacade.get_client(exc.KUCOIN)

es = [exc.KUCOIN,exc.CRYPTOPIA]


def history(e):
    market = "LTC_BTC"
    klines = afacade.get_candles_daily(market, e)    
    for x in klines:
        #ts,o,h,l,c = x
        #print (ts)
        #dt = models.conv_timestamp_tx(ts, exc.CRYPTOPIA)        
        #print (dt,o,h,l,c)
        #print (dt,c)
        print (x)
        

for e in es:
    history(e)
