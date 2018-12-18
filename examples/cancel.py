""" 
cancel tool. ask user for each open order if to cancel
"""

import sys
import archon
import archon.facade as facade
import archon.arch as arch
import archon.model.models as m
import archon.exchange.exchanges as exc
import time
import datetime
from util import *

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC,exc.BINANCE]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def cancel_exc(e):
    """ list open order and ask to cancel """
    oo = a.afacade.open_orders(e)
    n = exc.NAMES[e]
    print ("%s open orders %s" % (n,str(oo)))
    
    k = "otype"    
    open_bids = list(filter(lambda d: d[k]=="bid", oo))
    open_asks = list(filter(lambda d: d[k]=="ask", oo))

    ok = m.o_key_price(e)
    open_bids = sorted(open_bids, key=lambda k: ok,reverse=True) 
    open_bids = sorted(open_bids, key=lambda k: ok) 

    i = 0
    print ("bids " + str(open_bids))
    for o in open_bids:
        result = ask_user("cancel " + str(o) + " ? ")
        if result:
            print ("cancelling")
            k = m.o_key_id(e)
            oid = o[k]
            result = afacade.cancel(oid, e)
            print ("result" + str(result))
        else:
            print ("no")

    i = 0
    print ("asks " + str(open_asks))
    for o in open_asks:
        result = ask_user("cancel " + str(o) + " ? ")
        if result:
            print ("cancelling " + str(o))
            k = a.afacade.o_key_id(e)
            oid = o[k]
            result = a.afacade.cancel(oid, e)
            print ("result " + str(result))
        else:
            print ("no")


def cancel_indiviual():
    e1 = exc.CRYPTOPIA 
    #e2 = exc.BITTREX
    e1 = exc.BINANCE
    for e in [e1]:
        cancel_exc(e)

def cancel_all():
    a.cancel_all()


if __name__=='__main__': 
    #cancel_all()
    cancel_indiviual()
