""" 
cancel tool. ask user for each open order if to cancel
"""

import sys, os
import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import time
import datetime
from util import *

a = arch.Arch()
a.set_keys_exchange_file()

if __name__=='__main__': 

    for exchange in exc.supported_exchanges:
        oo = a.abroker.open_orders(exchange)
        n = exc.NAMES[exchange]
        print ("** %s open orders **"%n)
        print (len(oo))
        for o in oo:
            print (str(o))
    
    #########
    
    oo = a.global_openorders()    
    print ("all orders ",oo)
