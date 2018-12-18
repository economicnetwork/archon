import sys
import archon.facade as facade
import archon.broker as broker
import archon.model.models as m
import archon.exchange.exchanges as exc
from archon.util import *

import time
import datetime

from util import *
#from order_utils import *

import math

a = broker.Broker()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def ordering():       
    market = m.get_market("LTC","BTC",e)
    b = a.afacade.balance_all(exchange=e)
    
    #buy order
    #send 50% of qty to 1 exchange and 50% to another
    #check the amount possible to buy
    qty1 = 0.5*qty
    qty2 = 0.5*qty 


    
if __name__=='__main__':
    ordering()
