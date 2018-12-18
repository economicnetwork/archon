"""
broker warehouse
unifies any data for exchanges

transactions
orderbook

balances
"""

import archon.facade as facade
import archon.broker as broker
import archon.model.models as model
import archon.mongodb as mongodb
import archon.exchange.exchanges as exc
import archon.markets as markets
import archon.tx as tx
import time
from datetime import datetime

from archon.util import setup_logger

import math


logpath = './log'
log = setup_logger(logpath, 'info_logger', 'warehouse')

#afacade = facade.Facade()
#broker.setClientsFromFile(afacade)


def total_value(balances):
    total_all = 0
    for x in balances:
        total_all += x['USDvalue']

    total_all = round(total_all,2)
    return total_all

def store_balances(db, balances):    
    #mongodb.insert_balance(balances)
    #db.balances.drop()
    date_report_format = "%Y-%m-%d:%H:%M:%S"
    ds = datetime.now().strftime(date_report_format)
    total = total_value(balances)
    bd = {'balance_items':balances,'timestamp':ds,'total':total}
    #balances["timestamp"] = ds
    db.balances.insert(bd)

def get_balances_latest(db):
    b = list(db.balances.find().sort('timestamp').limit(1))[0]
    return b

def get_balances(db):
    #latest
    b = list(db.balances.find())    
    return b





