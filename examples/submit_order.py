import sys
import archon.broker as broker
import archon.arch as arch
import archon.model.models as m
import archon.exchange.exchanges as exc
from archon.util import *

import time
import datetime

from util import *
#from order_utils import *

import math

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def ordering(e):       
    market = m.get_market("LTC","BTC",e)
    b = a.abroker.balance_all(exchange=e)
    print ("balance ",b)
    print ("market " + market)    
    s = a.abroker.get_market_summary(market, e)
    print ("s ",s)
    bid = s["bid"]    
    ask = s["ask"]
    trade_type = "BUY"
    rho = 0.1
    price = bid * (1-rho)
    qty =  0.01
    o = [market, trade_type, price, qty]
    print ("order " + str(o))
    #r = abroker.submit_order(o,e)
    #print ("result " + str(r))

if __name__=='__main__':
    es = [exc.BITTREX,exc.CRYPTOPIA]
    for e in es:
        ordering(e)
