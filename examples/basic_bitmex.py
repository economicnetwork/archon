"""
basic trading
"""

import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as mex
import time

abroker = Brokerservice()
user_email = "ben@enet.io"

abroker.set_apikeys_fromfile(user_id="ben")
abroker.activate_session(user_id="ben")

abroker.set_client(exc.BITMEX)

def top_book():
    mex_client = abroker.get_client(exc.BITMEX)
    book = mex_client.market_depth(mex.instrument_btc_perp)
    mex_bids,mex_asks = [b for b in book if b['side']=='Buy'],[b for b in book if b['side']=='Sell']

    print ('***%s exchange***'%"BITMEX")
    topbid_mex = float(mex_bids[0]['price'])
    topask_mex = float(mex_asks[-1]['price'])
    mid_mex = (topbid_mex + topask_mex)/2
    print (topbid_mex,topask_mex,mid_mex)

if __name__=='__main__':
    while True:
        top_book()
        time.sleep(5)
