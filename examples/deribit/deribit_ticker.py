"""
find options of deribit
"""

from archon.exchange.deribit.Wrapper import DeribitWrapper
import archon.config as config

from datetime import datetime
import time

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)
time.sleep(5)

if __name__=='__main__':  
    print ("start....")              
    s = 'BTC-PERPETUAL'
    summary = w.getsummary(s)
    #'bidPrice': 3655.0, 'askPrice': 3655.5,
    bid,ask = summary['bidPrice'],summary['askPrice']
    print ("ticker: ",bid,ask)


    #d = w.json_depth(s)
    #print (d)
"""
BTC-PERPETUAL
BTC-28JUN19
BTC-29MAR19
"""    