from numpy import array
import pandas as pd

def convert_dataframe(candle_array):
    """ convert an array to pandas df """
    
    opens = [float(z['open']) for z in candle_array]
    high = [float(z['high']) for z in candle_array]
    low = [float(z['low']) for z in candle_array]
    closes = [float(z['close']) for z in candle_array]
    volumes = [float(z['volume']) for z in candle_array]
    dates = [z['timestamp'] for z in candle_array]

    raw_data = {'open':opens,'high':high,'low':low,'close':closes,'volume': volumes}
    df = pd.DataFrame(raw_data, index=dates, columns = ['open','high','low','close','volume'])    
    return df