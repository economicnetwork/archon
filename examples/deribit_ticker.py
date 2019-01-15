"""
find options of deribit
"""

from archon.ws.deribit.Wrapper import DeribitWrapper
import archon.config as config

from datetime import datetime

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

if __name__=='__main__':                
    s = 'BTC-PERPETUAL'
    summary = w.getsummary(s)
    #'bidPrice': 3655.0, 'askPrice': 3655.5,
    bid,ask = summary['bidPrice'],summary['askPrice']
    print ("??? ",bid,ask)

"""
BTC-PERPETUAL
BTC-28JUN19
BTC-29MAR19
"""    