import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import datetime
from loguru import logger

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

candles = client.trades_candle("XBTUSD")
candles.reverse()

for x in candles:
    t,c = x['timestamp'],x['close']
    print (t,c)