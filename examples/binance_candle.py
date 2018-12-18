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

market = models.market_from("RVN","BTC")

x = a.afacade.get_candles_hourly(market,exc.BINANCE)

for z in x[-10:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    print (ts,c,z[5])

