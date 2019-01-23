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

from arctic import Arctic
import quandl

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

candles = client.trades_candle("XBTUSD", mex.candle_1d)
candles.reverse()

# Connect to Local MONGODB
store = Arctic('localhost')

# Create the library - defaults to VersionStore
store.initialize_library('NASDAQ')

# Access the library
library = store['NASDAQ']

library.write('XBTUSD', candles, metadata={'source': 'Bitmex'})

# Reading the data
item = library.read('XBTUSD')
xbtusd = item.data
#metadata = item.metadata

print (xbtusd)