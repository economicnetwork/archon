import pandas as pd
import talib
import numpy
import matplotlib.pyplot as plt

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

market = models.market_from("ADA","BTC")

#x = a.afacade.get_candles_hourly(market,exc.BINANCE)
data = a.afacade.get_candles_daily(market,exc.BINANCE)

closes = list()
COL_CLOSE = 4
COL_VOLUME = 5

"""
for z in x[-100:]:
    ts = z[0]
    o,h,l,c = z[1:5]
    print (ts,c,z[5])
    closes.append(c)
"""    

from numpy import array
closes = [float(z[COL_CLOSE]) for z in data]
#closes = numpy.array(float_data)

volumes = [float(z[COL_VOLUME]) for z in data]
#print (volumes)
#volumes = numpy.array(float_data)

#sma = talib.RSI(closes)

raw_data = {'close': closes, 'volume': volumes, }
df = pd.DataFrame(raw_data, columns = ['close', 'volume'])

df['Mavg5'] = df['close'].rolling(window=5).mean()
df['Mavg20'] = df['close'].rolling(window=20).mean()

print (df)

prev_short_mavg = df['Mavg5'].shift(1)
prev_long_mavg = df['Mavg20'].shift(1)
 
# Select buying and selling signals: where moving averages cross
buys = df.ix[(df['Mavg5'] <= df['Mavg20']) & (prev_short_mavg >= prev_long_mavg)]
sells = df.ix[(df['Mavg5'] >= df['Mavg20']) & (prev_short_mavg <= prev_long_mavg)]

# The label parameter is useful for the legend
plt.plot(df.index, df['close'], label='price')
plt.plot(df.index, df['Mavg5'], label='5-day moving average')
plt.plot(df.index, df['Mavg20'], label='20-day moving average')

plt.plot(buys.index, df.ix[buys.index]['close'], '^', markersize=10, color='g')
plt.plot(sells.index, df.ix[sells.index]['close'], 'v', markersize=10, color='r')

plt.ylabel('price')
plt.xlabel('Date')
plt.legend(loc=0)
plt.show()

