import matplotlib.pyplot as plt
import archon.facade as facade
import archon.arch as arch
import archon.exchange.exchanges as exc
import archon.model.models as models
from archon.util import *
import datetime
import numpy as np


a = arch.Arch()
a.set_keys_exchange_file()
client = a.afacade.get_client(exc.BINANCE)

market = models.market_from("LTC","BTC")

x = a.afacade.get_candles_hourly(market,exc.BINANCE)

candles = list()
xs = list()
for z in x[:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    candles.append(c)
    xs.append(ts)

plt.plot(xs,candles)

ax = plt.gca()
ax.invert_yaxis()
plt.show()