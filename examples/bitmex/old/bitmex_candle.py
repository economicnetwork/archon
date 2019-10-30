import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import datetime

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

candles = client.trades_candle("XBTUSD", mex.candle_1d)
candles.reverse()

for x in candles[-10:]:
    t,c = x['timestamp'],x['close']
    print (t,c)

time.sleep(1)

candles = client.trades_candle("XBTUSD", mex.candle_1m)
candles.reverse()

for x in candles[-10:]:
    t,c = x['timestamp'],x['close']
    print (t,c)    