"""
buy up or sell holdings slowly depending on volume
Binance

example:
LTC/BTC
* buy with 25 btc at a price no more than x with 5% of current volume

algorithm details:
* get daily volume of the last 30 days
* use average volume as expectation for tomorrows volume
* buy x% of the daily volume spread over day

export PYTHONPATH=/Users/x/archon
"""

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

market = models.market_from("LTC","BTC")

x = abroker.get_candles_hourly(market,exc.BINANCE)

for z in x[-10:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    print (ts,c,z[5])





