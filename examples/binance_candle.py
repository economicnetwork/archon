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

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
client = abroker.get_client(exc.BINANCE)

market = models.market_from("RVN","BTC")

x = abroker.get_candles_hourly(market,exc.BINANCE)

for z in x[-10:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    print (ts,c,z[5])

