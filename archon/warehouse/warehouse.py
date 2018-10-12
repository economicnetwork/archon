"""
broker warehouse
unifies any data for exchanges

transactions
orderbook

balances
"""

import archon.broker as broker
import archon.arch as arch
import archon.model.models as model
import archon.mongodb as mongodb
import archon.exchange.exchanges as exc
import archon.markets as markets
import archon.tx as tx
import time
from datetime import datetime

from archon.util import setup_logger

import math

import logging
import os

def setup_logger(logpath, name, log_file, level=logging.INFO):    
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    
    #logPath = "./"
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logpath, log_file)),
        logging.StreamHandler()
    ])
    formatter = logging.Formatter('%(asctime)s,%(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


logpath = './log'
log = setup_logger(logpath, 'info_logger', 'warehouse')

#abroker = broker.Broker()
#arch.setClientsFromFile(abroker)


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





"""
def tx_history_converted(nom, denom, exchange):
    if exchange == exc.CRYPTOPIA:   
        market = markets.get_market(nom,denom,exchange) 
        txs = abroker.market_history(market,exchange)
        txs.reverse()
        new_txs_list = list() 
        print (len(txs))   
        for txitem in txs[:]:
            #print ("convert "+ str(txitem))
            txd = model.convert_tx(txitem, exc.CRYPTOPIA, market)
            new_txs_list.append(txd)
        return new_txs_list
    elif exchange == exc.BITTREX:  
        market = markets.get_market(nom,denom,exc.BITTREX)
        txs = abroker.market_history(market,exc.BITTREX)
        txs.reverse()
        #log.info("txs " + str(txs[:3]))    
        new_txs_list = list()            
        for txitem in txs[:]:
            txd = model.convert_tx(txitem, exc.BITTREX, market)
            new_txs_list.append(txd)
        return new_txs_list

    elif exchange == exc.KUCOIN:  
        market = markets.get_market(nom,denom,exc.KUCOIN)
        txs = abroker.market_history(market,exc.KUCOIN)
        new_txs_list = list()
        for txitem in txs:
            txd = model.convert_tx(txitem, exchange, market)
            new_txs_list.append(txd)
        return new_txs_list
"""            
        


