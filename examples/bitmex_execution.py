import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import datetime
from loguru import logger

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)

exe = client.execution_history()
for x in exe:
    print (x['timestamp'],x['side'],x['orderQty'],x['realisedPnl'],x['unrealisedPnl'])
    #print (x)

#print (exe)