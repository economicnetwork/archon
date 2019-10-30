import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.facade as facade
import archon.model.models as models
from archon.util import *

import pandas as pd
import numpy
import matplotlib.pyplot as plt
from arctic import Arctic


abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file(exchanges=[exc.BITMEX])
#abroker.set_active_exchanges([exc.BITMEX])

def get_candle_pandas():
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
    return df

def show():        
    # Connect to Local MONGODB
    store = Arctic('localhost')
    # Create the library - defaults to VersionStore
    store.initialize_library('Bitmex')
    # Access the library
    library = store['Bitmex']
    #library.write('XBTUSD', df, metadata={'source': 'Bitmex'})

    # Reading the data
    item = library.read('XBTUSD')
    xbtusd = item.data
    metadata = item.metadata
    print (xbtusd)
    print (metadata)
    
    xbtusd['ret'] = -1+xbtusd['close']/xbtusd['close'].shift(1)

    from math import sqrt
    xbtusd['vol10'] = sqrt(260)*xbtusd['ret'].rolling(10).std(ddof=0)
    xbtusd['vol30'] = sqrt(260)*xbtusd['ret'].rolling(30).std(ddof=0)

    #print (volList)

    #plt.plot(df.index, df['close'], label='price')
    plt.plot(xbtusd.index, xbtusd['vol10'], label='vol10')
    plt.plot(xbtusd.index, xbtusd['vol30'], label='vol30')
    #plt.plot(xbtusd['ret'])
    plt.ylabel('vol')
    plt.xlabel('Date')
    plt.legend(loc=0)

    plt.show()


def sync():
    store = Arctic('localhost')
    store.initialize_library('Bitmex')
    library = store['Bitmex']
    df = get_candle_pandas()
    print (df)
    library.write('XBTUSD', df, metadata={'source': 'Bitmex'})

if __name__=='__main__':
    show()

