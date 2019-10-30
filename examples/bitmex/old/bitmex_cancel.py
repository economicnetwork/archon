import logging
import os
import time

import numpy
from pymongo import MongoClient
import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as m

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

def cancel_all():
    oo = abroker.afacade.open_orders(exc.BITMEX)
    if len(oo)>0:
        for o in oo:
            oid = o['orderID']
            result = abroker.cancel_order(oid, exc.BITMEX)
            print (result)


if __name__ == '__main__':  
    cancel_all()