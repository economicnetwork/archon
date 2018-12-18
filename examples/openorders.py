""" 
cancel tool. ask user for each open order if to cancel
"""

import sys, os
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import time
import datetime
from util import *

a = broker.Broker()
a.set_keys_exchange_file()

if __name__=='__main__': 
    
    for exchange in a.active_exchanges:
        oo = a.afacade.open_orders(exchange)
        n = exc.NAMES[exchange]
        print ("** %s open orders **"%n)
        if oo:
            print (len(oo))
            for o in oo:
                print (str(o))
    
    #########
    
    oo = a.global_openorders()    
    print ("all orders ",oo)
