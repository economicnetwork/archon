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
while True:
    oo = abroker.afacade.open_orders(exc.BITMEX)
    print (oo)
    for o in oo:
        print (o['ordStatus'])
    time.sleep(10)
