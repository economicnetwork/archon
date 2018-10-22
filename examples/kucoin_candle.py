import sys
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.model.models as models

import pandas


abroker = broker.Broker()
arch.setClientsFromFile(abroker)
client = abroker.get_client(exc.KUCOIN)

e = exc.KUCOIN

def history_daily():
    #res = client.RESOLUTION_1MINUTE
    market = "TOMO-BTC"
    klines = abroker.get_candles_daily(market, e)    
    for x in klines:
        ts,o,h,l,c,v = x
        dt = models.conv_timestamp_tx(ts, exc.KUCOIN)        
        print (dt,o,h,l,c)

def history_hourly():
    market = "GO-ETH"
    klines = abroker.get_candles_hourly(market, e)    
    for x in klines:
        ts,o,h,l,c,v = x
        dt = models.conv_timestamp_tx(ts, exc.KUCOIN)        
        print (dt,o,h,l,c)


history_hourly()
