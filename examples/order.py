import sys
sys.path.append('/Users/ben/archon')
import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
from archon.util import *

import time
import datetime

from util import *
#from order_utils import *

import math

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

def ordering():   
    market ="BTC-ETH" 
    print ("market " + market)
    e = exc.BITTREX
    s = abroker.get_market_summary_str(market, e)
    kb = abroker.bid_key(e)
    ka = abroker.ask_key(e)
    bid = s[k]    
    ask = s[ka]
    trade_type = "BUY"
    pip = 0.00000001
    price = bid + pip
    qty =  1.23
    o = [market, trade_type, price, qty]
    print ("order " + str(o))
    r = abroker.submit_order(o,e)
    print ("result " + str(r))

if __name__=='__main__':
    ordering()
