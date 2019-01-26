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
    #'2019-01-09T14:29:10.136Z'
    dt1 = datetime.datetime.strptime(t1[:-5],'%Y-%m-%dT%H:%M:%S')
    dt2 = datetime.datetime.strptime(t2[:-5],'%Y-%m-%dT%H:%M:%S')
    td = dt2-dt1

    ret = first['price']/last['price'] -1
    sec = td.seconds
    trade_sec = round(100/sec,3)
    print (len(buys),len(sells),sumbuy,sumsell,lastprice,ret,dt1,dt2,td.seconds,trade_sec)
    time.sleep(5)