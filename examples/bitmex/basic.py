"""
basic trading
"""

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
    broker.set_client(exc.BITMEX)  
    return broker

def top_book():  
    mex_client = broker.get_client(exc.BITMEX)
    book = mex_client.market_depth(mex.instrument_btc_perp)
    mex_bids,mex_asks = [b for b in book if b['side']=='Buy'],[b for b in book if b['side']=='Sell']

    print ('***%s exchange***'%"BITMEX")
    topbid_mex = float(mex_bids[0]['price'])
    topask_mex = float(mex_asks[-1]['price'])
    mid_mex = (topbid_mex + topask_mex)/2
    print (topbid_mex,topask_mex,mid_mex)

if __name__=='__main__':   
    setup_broker() 
    while True:
        top_book()
        time.sleep(5)
