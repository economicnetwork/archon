import sys
import archon.facade as facade
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

def ordering():       
    currency = input("what market against BTC? ")
    e = input("what exchange (number)? CRYPTOPIA = 0 BITTREX = 1 KUCOIN = 2 BINANCE = 3 KRAKEN = 4 HITBTC = 5")
    e = int(e)
    market = m.get_market(currency,"BTC",e)
    buysell = input("buy or sell? ")
    qty = input("quantity? ")
    qty = float(qty)

    b = a.afacade.balance_all(exchange=e)
    btc_balance = list(filter(lambda x: x['symbol'] == 'BTC', b))[0]['amount']
    print (btc_balance)
    s = a.afacade.get_market_summary(market, e)
    bid = s["bid"]    
    ask = s["ask"]
    
    if buysell == "BUY":
        if btc_balance > 0.001:                
                trade_type = "BUY"
                rho = 0.1
                price = round(bid * (1-rho),8)
                print ("target price ",price)
                #qty =  0.1
                market = m.market_from(currency,"BTC",)
                o = [market, trade_type, price, qty]
                print ("order " + str(o))
                r = a.afacade.submit_order(o,e)
                print ("order result " + str(r))
        else:
            print ("insufficient balance")
    else:
        #TODO check LTC balance
        trade_type = "SELL"
        rho = 0.001
        price = round(ask * (1-rho),8)
        print ("target price ",price)
        #qty =  0.1        
        market = m.market_from(currency,"BTC")
        o = [market, trade_type, price, qty]
        print ("order " + str(o))
        r = a.afacade.submit_order(o,e)
        print ("order result " + str(r))

if __name__=='__main__':
    ordering()
