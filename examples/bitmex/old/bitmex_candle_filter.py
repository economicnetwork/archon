import argparse
import json
import csv
import sys
import time

import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import datetime
import pandas as pd

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)


def convert_pandas(candles):
    COL_OPEN = 'open'
    COL_HIGH = 'high'
    COL_LOW = 'low'
    COL_CLOSE = 'close'
    COL_VOLUME = 'volume'
    
    opens = [float(z[COL_OPEN]) for z in candles]
    highs = [float(z[COL_HIGH]) for z in candles]
    lows = [float(z[COL_LOW]) for z in candles]
    closes = [float(z[COL_CLOSE]) for z in candles]
    volumes = [float(z[COL_VOLUME]) for z in candles]
    dates = [z['timestamp'] for z in candles]

    raw_data = {COL_OPEN: opens, COL_HIGH: highs, COL_LOW: lows, COL_CLOSE: closes, COL_VOLUME: volumes}
    df = pd.DataFrame(raw_data, index=dates, columns = [COL_OPEN, COL_HIGH, COL_LOW, COL_CLOSE, COL_VOLUME])
    return df

def get_candle_pandas():
    client = abroker.afacade.get_client(exc.BITMEX)
    candles = client.trades_candle("XBTUSD", mex.candle_1d)
    candles.reverse()
    df = convert_pandas(candles)
    return df


df = get_candle_pandas()
df['change'] = -1+df['close']/df['close'].shift(1)

filtered = df.loc[(df['change'] >= 0.05)]
#print (df)
print (filtered)
