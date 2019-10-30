"""
"""

import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as mex
import time
from util import *
import argparse
import json
import csv
import sys

#import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import datetime

broker = Brokerservice()

def setup_broker():
    user_id = parse_toml("conf.toml")["user_id"]
    broker.set_apikeys_fromfile(user_id)
    broker.activate_session(user_id)
    broker.set_client(exc.BITMEX)  
    return broker

if __name__=='__main__': 
    setup_broker()
    mex_client = broker.get_client(exc.BITMEX)

    print('trade history')
    print ("len(buys), len(sells) , sumbuy, sumsell, lastprice, return , t1, t2, delta seconds, trades/second")
    print ('*'*20)
        
    trades = mex_client.recent_trades("XBTUSD")
    for x in trades:
        print (x)

    print ("total trades %i"%len(trades))