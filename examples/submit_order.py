import sys
import archon.facade as facade
import archon.arch as arch
import archon.model.models as m
import archon.exchange.exchanges as exc
from archon.util import *
logpath = './log'
log = setup_logger(logpath, 'archon_logger', 'archon')


import time
import datetime

from util import *
#from order_utils import *

import math



a = arch.Arch()
#ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
ae = [exc.BINANCE]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def ordering(e):       
    #market = m.get_market("LTC","BTC",e)
    market = m.market_from("LTC","BTC")
    b = a.afacade.balance_all(exchange=e)
    btc_balance = list(filter(lambda x: x['symbol'] == 'BTC', b))[0]['amount']
    print (btc_balance)

    #b = a.afacade.balance_currency("BTC",e)
    if btc_balance > 0.001:
        print ("balance ",b)
        print ("market " + market)    
        s = a.afacade.get_market_summary(market, e)
        print ("s ",s)
        bid = s["bid"]    
        ask = s["ask"]
        trade_type = "BUY"
        rho = 0.03        
        rounding = 8
        if e == exc.BINANCE:
            #binance rounds to 6
            rounding = 6
        price = round(bid * (1-rho),rounding)
        qty =  0.5
        
        o = [market, trade_type, price, qty]
        print ("order " + str(o))
        r = a.afacade.submit_order(o,e)
        print ("order result " + str(r))
    else:
        print ("insufficient balance")

if __name__=='__main__':
    #es = [exc.BITTREX, exc.HITBTC]
    es = [exc.BINANCE]
    for e in es:
        ordering(e)
