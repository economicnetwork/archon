import argparse
import json
import csv
import sys
import time

import numpy
from pymongo import MongoClient
import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

trades = client.recent_trades("XBTUSD")
buys = list(filter(lambda x: x['side']=='Buy',trades))
sells = list(filter(lambda x: x['side']=='Sell',trades))

sumbuy = sum(list(map(lambda x: x['size'], buys)))
sumsell = sum(list(map(lambda x: x['size'], sells)))

print ("buys ",len(buys))
print ("sell ",len(sells))
print ("sumbuy ",sumbuy)
print ("sumsell ",sumsell)

print (trades[-1])

for x in trades:
    print (x)