import sys
import archon.facade as facade
import archon.arch as arch
import archon.markets as markets
import archon.model.models as m
import archon.exchange.exchanges as exc
from archon.util import *

import time
import datetime

from util import *
#from order_utils import *

import math



import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch

afacade = facade.Facade()
arch.setClientsFromFile(afacade)

bl = list()
for e in [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.BINANCE]:
    b = afacade.balance_all(exchange=e)
    for x in b:
        n = exc.NAMES[e]
        x['exchange'] = n
        s = x['symbol']
        t = float(x['total'])
        if t > 0:
            print (x)



def ordering(e):       
    market = markets.get_market("ETH","BTC",e)
    print ("market " + market)    
    s = afacade.get_market_summary_str(market, e)
    kb = m.bid_key(e)
    ka = m.ask_key(e)
    bid = s[kb]    
    ask = s[ka]
    trade_type = "BUY"
    pip = 0.00000001
    rho = 0.1
    price = bid * (1-rho)
    qty =  1.23
    o = [market, trade_type, price, qty]
    print ("order " + str(o))
    #r = afacade.submit_order(o,e)
    print ("result " + str(r))

"""
if __name__=='__main__':
    #e = exc.BITTREX
    es = [exc.BITTREX,exc.CRYPTOPIA]
    for e in es:
        ordering(e)
"""