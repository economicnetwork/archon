"""
broker warehouse
unifies any data for exchanges

transactions
orderbook

balances
"""

import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.markets as markets
import archon.tx as tx
import time
import datetime

from archon.util import *

import math

logpath = './log'
log = setup_logger(logpath, 'info_logger', 'warehouse')

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

# store tx

def tx_history_converted(market, exchange):
    if exchange == exc.CRYPTOPIA:    
        txs = abroker.market_history(market,exchange)
        txs.reverse()
        new_txs_list = list()    
        for txitem in txs[:]:
            #print ("convert "+ str(txitem))
            txd = tx.convert(txitem, exc.CRYPTOPIA, market)
            new_txs_list.append(txd)
        return new_txs_list
    elif exchange == exc.BITTREX:  
        rexmarket = markets.convert_markets_from(market,exc.BITTREX)
        txs = abroker.market_history(rexmarket,exc.BITTREX)
        txs.reverse()
        #log.info("txs " + str(txs[:3]))    
        new_txs_list = list()            
        for txitem in txs[:]:
            txd = tx.convert(txitem, exc.BITTREX, market)
            new_txs_list.append(txd)
        return new_txs_list

    """
    ts = tx['Timestamp']
    tsf = datetime.datetime.fromtimestamp(ts).strftime('%D %H:%M:%S')
    ty = tx['Type']
    p = tx['Price']
    """

