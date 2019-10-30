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

ts = "2019-01-12" + "T12:00:00.000Z"
symbol = "XBTUSD"
exe = client.execution_history(symbol, ts)

mk = ['side','orderQty','price','commission','execCost','timestamp']
exe.reverse()
print ("side,orderQty,price,commission,execCost,timestamp")
for x in exe:
    if x['ordStatus'] != 'Filled': continue
    #print (x)
    if x['side']=='': continue
    s = ""
    for k,v in x.items():
        if k in mk:
            #print (k, " ",v)
            s += str(v)+","
    print (s)
    #'execCost': -54976, 'execComm': -13
    #print (x['timestamp'],x['side'],x['cumQty'],x['price'])    

#print (exe[-1].keys())

"""
{'execID': 'orderID': 
'clOrdID':  'clOrdLinkID': '', 'account': 722235,
 'symbol': 'XBTUSD', 'side': 'Buy', 'lastQty': 2, 'lastPx': 3626, 'underlyingLastPx': None,
  'lastMkt': 'XBME', 'lastLiquidityInd': 'AddedLiquidity', 'simpleOrderQty': None, 
  'orderQty': 2, 'price': 3626, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 
  'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'execType': 'Trade',
   'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '',
    'exDestination': 'XBME', 'ordStatus': 'Filled', 'triggered': '', 'workingIndicator': False, 
    'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 0, 'simpleCumQty': None, 
    'cumQty': 2, 'avgPx': 3626, 'commission': -0.00025, 'tradePublishIndicator': 
    'PublishTrade', 'multiLegReportingType': 'SingleSecurity', 'text':
     'trdMatchID': 'dff6d536-074c-afb6-feef-b57c41884a5d', 'execCost': -55158, 
     'execComm': -13, 'homeNotional': 0.00055158, 'foreignNotional': -2, 
     'transactTime': '2019-01-11T10:35:42.970Z', 
     'timestamp': '2019-01-11T10:35:42.970Z'}
"""     