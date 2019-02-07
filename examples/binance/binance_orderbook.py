import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.binance as b
import archon.model.models as models
from archon.util import *

import time
import datetime
import math

from datetime import datetime

a = broker.Broker()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)
market = models.get_market("REP","ETH",exc.BINANCE)
[bids,asks] = a.afacade.get_orderbook(market,exc.BINANCE)
print (bids[0],asks[0])

"""
#print (market)
m = models.market_from("REP","ETH")
print (m)
#x = client.get_orderbook_symbol(market)
#print (x)
"""