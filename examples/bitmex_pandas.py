import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.facade as facade
import archon.model.models as models
from archon.util import *

import pandas as pd
import numpy
import matplotlib.pyplot as plt

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)
candles = client.trades_candle("XBTUSD", mex.candle_1d)
candles.reverse()

closes = list()
COL_CLOSE = 'close'
COL_VOLUME = 'volume'

from numpy import array
closes = [float(z[COL_CLOSE]) for z in candles]
volumes = [float(z[COL_VOLUME]) for z in candles]
dates = [z['timestamp'] for z in candles]

raw_data = {'close': closes, 'volume': volumes}

df = pd.DataFrame(raw_data, index=dates, columns = ['close', 'volume'])
#df = df.iloc[::2, :]

print (df)
plt.plot(df.index, df['close'], label='price')
plt.show()

