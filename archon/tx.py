
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


