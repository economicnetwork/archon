"""
find options of deribit
"""

from archon.exchange.deribit.Wrapper import DeribitWrapper

from datetime import datetime
import time

import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as mex
import time
from util import *

broker = Brokerservice()

def setup_broker():
    user_id = parse_toml("conf.toml")["user_id"]
    broker.set_apikeys_fromfile(user_id)
    broker.activate_session(user_id)
    broker.set_client(exc.DERIBIT)  
    return broker

if __name__=='__main__':  
    print ("start....")
    setup_broker()
    deribit_client = broker.get_client(exc.DERIBIT)
    s = 'BTC-PERPETUAL'
    summary = deribit_client.getsummary(s)
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