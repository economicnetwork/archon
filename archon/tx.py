
"""
Bittrex
{'Id': 283006714, 'TimeStamp': '2018-09-26T09:04:34.273', 'Quantity': 0.15985865, 'Price': 0.03288274, 'Total': 0.00525659, 'FillType': 'PARTIAL_FILL', 'OrderType': 'SELL'}, 
tsf = tx['TimeStamp']
ty = tx['OrderType']
"""

import archon.exchange.exchanges as exc
import archon.markets as markets
import pytz, datetime

date_broker_format = "%Y-%m-%d %H:%M:%S"


#def toUTC(d):
#    tz = pytz.timezone ("Europe/Berlin") 
#    return tz.normalize(tz.localize(d)).astimezone(pytz.utc)

def conv_timestamp(ts, exchange):    
    if exchange==exc.CRYPTOPIA:
        #local = pytz.timezone("Europe/London") 
        #tsf = datetime.datetime.fromtimestamp(ts)
        tsf = datetime.datetime.utcfromtimestamp(ts)        
        #local_dt = local.localize(tsf, is_dst=None)
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        #dt = utc_dt.strftime(date_broker_format)        
        
        return utc_dt
    elif exchange==exc.BITTREX:
        ts = ts.split('.')[0]
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        return utc_dt


def convert(tx, exchange, market):
    """ convert transaction """
    if exchange==exc.CRYPTOPIA:
        #CET time        
        ts = tx['Timestamp']
        dt = conv_timestamp(ts, exchange)
        #print (ts,dt)
        ty = tx['Type']
        p = tx['Price']
        market = tx['Label']
        conv_market = markets.convert_markets_to(market, exchange)
        #print (conv_market)
        d = {'timestamp': dt, 'txtype': ty,'price':p,'exchange':exchange,'market':conv_market}
        return d
    elif exchange==exc.BITTREX:
        #UTC time
        ts = tx['TimeStamp']
        dt = conv_timestamp(ts, exchange)
        ty = convert_type_key(tx['OrderType'], exchange)
        p = tx['Price']
        d = {'timestamp': dt, 'txtype': ty,'price':p,'exchange':exchange,'market':market}
        return d

def convert_type_key(key, exchange):
    if exchange==exc.CRYPTOPIA:
        return key
    elif exchange==exc.BITTREX:    
        if key == 'BUY': 
            return 'Buy'
        else:
            return 'Sell'

def buy_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return 'Buy'
    elif exchange==exc.BITTREX:    
        return 'BUY'

def sell_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return 'Sell'
    elif exchange==exc.BITTREX:    
        return 'SELL'

def timestamp_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return 'Timestamp'
    elif exchange==exc.BITTREX:    
        return 'TimeStamp'

def otype_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return 'Type'
    elif exchange==exc.BITTREX:    
        return 'OrderType'


