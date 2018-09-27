""" 
cancel tool. ask user for each open order if to cancel
"""

import sys
#sys.path.append('/Users/x/archon')
import archon
import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import time
import datetime

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

def cancel_exc(e):
    """ list open order and ask to cancel """
    oo = abroker.open_orders_all(e)
    print ("open orders " + str(oo))
    
    k = abroker.otype_key(e)
    k_buy = abroker.otype_key_buy(e)
    k_sell = abroker.otype_key_sell(e)
    open_bids = [o for o in oo if k==k_buy]
    open_asks = [o for o in oo if k==k_sell]

    ok = abroker.o_key_price(e)
    open_bids = sorted(open_bids, key=lambda k: ok,reverse=True) 
    open_asks = sorted(open_asks, key=lambda k: ok) 

    i = 0
    for o in open_bids:
        result = ask_user("cancel " + str(o) + " ? ")
        if result:
            print ("cancelling")
            k = abroker.o_key_id(e)
            oid = o[k]
            result = abroker.cancel(order_id, exc.CRYPTOPIA)
            print ("result" + str(result))
        else:
            print ("no")

    i = 0
    for o in open_asks:
        result = ask_user("cancel " + str(o) + " ? ")
        if result:
            print ("cancelling " + str(o))
            k = abroker.o_key_id(e)
            oid = o[k]
            result = abroker.cancel(order_id, exc.CRYPTOPIA)
            print ("result " + str(result))
        else:
            print ("no")

if __name__=='__main__': 
    e1 = exc.CRYPTOPIA 
    e2 = exc.BITTREX
    for e in [e1,e2]:
        cancel_exc(e)
    
