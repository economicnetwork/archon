import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.exchange.binance as b
import archon.model.models as models
from archon.util import *

import time
import datetime
import math

from datetime import datetime

a = arch.Arch()
a.set_keys_exchange_file()
client = a.abroker.get_client(exc.BINANCE)
market = models.get_market("RVN","BTC",exc.BINANCE)
x = client.get_orderbook_symbol(market)
time.sleep(0.5)
m = models.market_from("RVN","BTC")
[bids,asks] = a.abroker.get_orderbook(m,exc.BINANCE)
print (bids[0],asks[0])