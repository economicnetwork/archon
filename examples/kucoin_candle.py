import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch
import archon.model.models as models

import pandas


afacade = facade.Facade()
arch.setClientsFromFile(afacade)
client = afacade.get_client(exc.KUCOIN)

e = exc.KUCOIN

def history_daily():
    #res = client.RESOLUTION_1MINUTE
    market = "TOMO-BTC"
    klines = afacade.get_candles_daily(market, e)    
    for x in klines:
        ts,o,h,l,c,v = x
        dt = models.conv_timestamp_tx(ts, exc.KUCOIN)        
        print (dt,o,h,l,c)

def history_hourly():
    market = "GO-ETH"
    klines = afacade.get_candles_hourly(market, e)    
    for x in klines:
        ts,o,h,l,c,v = x
        dt = models.conv_timestamp_tx(ts, exc.KUCOIN)        
        print (dt,o,h,l,c)


history_hourly()
