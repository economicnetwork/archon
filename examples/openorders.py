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

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
abroker.set_active_exchanges(exc.supported_exchanges)

if __name__=='__main__': 

    for exchange in exc.supported_exchanges:
        oo = abroker.open_orders(exchange)
        n = exc.NAMES[exchange]
        print ("** %s open orders **"%n)
        print (len(oo))
        for o in oo:
            print (str(o))
    
    #########
    
    oo = abroker.all_open_orders()    
    print ("all orders ",oo)
