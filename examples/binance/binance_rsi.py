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

import talib
import numpy
import matplotlib.pyplot as plt

a = broker.Broker()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

market = models.market_from("ADA","BTC")

#x = a.afacade.get_candles_hourly(market,exc.BINANCE)
x = a.afacade.get_candles_daily(market,exc.BINANCE)

closes = list()

for z in x[-100:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    print (ts,c,z[5])
    closes.append(c)

from numpy import array
float_data = [float(x) for x in closes]
np_float_data = numpy.array(float_data)
closes = np_float_data
sma = talib.RSI(closes)

plt.subplot(2, 1, 1)
t = 'Price ' + str(market)
plt.title(t)
plt.plot(closes)
plt.subplot(2, 1, 2)
t = 'RSI ' + str(market)
plt.title(t)
plt.plot(sma)

plt.show()