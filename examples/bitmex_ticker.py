import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

print ("len(buys), len(sells) , sumbuy, sumsell, lastprice, return , t1, t2")
print ('*'*20)
while True:
    
    
    trades = client.recent_trades("XBTUSD")
    buys = list(filter(lambda x: x['side']=='Buy',trades))
    sells = list(filter(lambda x: x['side']=='Sell',trades))

    sumbuy = sum(list(map(lambda x: x['size'], buys)))
    sumsell = sum(list(map(lambda x: x['size'], sells)))

    lastprice = trades[-1]['price']

    first = trades[-1]
    last = trades[0]
    t1 = first['timestamp']
    t2 = last['timestamp']
    ret = first['price']/last['price'] -1
    print (len(buys),len(sells),sumbuy,sumsell,lastprice,ret,t1,t2)
    time.sleep(5)