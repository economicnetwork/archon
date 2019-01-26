import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import datetime

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

print ("len(buys), len(sells) , sumbuy, sumsell, lastprice, return , t1, t2, delta seconds, trades/second")
print ('*'*20)
    
trades = client.recent_trades("XBTUSD")
for x in trades:
    print (x)