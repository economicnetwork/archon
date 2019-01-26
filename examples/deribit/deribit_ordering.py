"""
find options of deribit
"""

import archon.config as config

from datetime import datetime

import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.book_util as book_util
import archon.exchange.bitmex.timeseries as timeseries
import archon.facade as facade
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from archon.util import *

import pandas as pd
import numpy

import redis
import time
import json

abroker = broker.Broker(setAuto=True)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT]) 
client = abroker.afacade.get_client(exc.DERIBIT)

sym = 'BTC-PERPETUAL'

def order():
    summary = client.getsummary(sym)
    deri_bid,deri_ask = summary['bidPrice'],summary['askPrice']
    r = w.buy(sym, 10, deri_bid-1,postOnly=True)
    print (r)

    r = w.sell(sym, 10, deri_bid+1,postOnly=True)
    print (r)

def cancel_all():
    oo = client.getopenorders(sym)
    print (oo)

    for o in oo:
        w.cancel(o['orderId'])

oo = client.getopenorders(sym)
print (oo)

#order()         
#[{'instrument': 'BTC-PERPETUAL', 'kind': 'future', 'size': 1, 'amount': 10.0, 
# 'averagePrice': 3631.99995351, 'direction': 'buy', 'sizeBtc': 0.002751599, 
# 'floatingPl': 1.705e-06, 'realizedPl': 0.000581306, 'estLiqPrice': 213.98, 
# 'markPrice': 3634.25, 'indexPrice': 3635.79, 'maintenanceMargin': 1.4446e-05, 
# 'initialMargin': 3.7835e-05, 'settlementPrice': 3663.85, 'delta': 0.002751599, 
# 'openOrderMargin': 0.0, 'profitLoss': 1.705e-06}]

#pos = w.positions()
#print ("pos ",pos)