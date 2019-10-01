import requests
import json
import os

from archon.exchange.delta.delta_rest_client import create_order_format, cancel_order_format, round_by_tick_size
from archon.exchange.delta.instruments import btc_march, btc_march_quanto, btc_june, product_names
import archon.exchange.exchanges as exc
from archon.plugins.aws_ses import AwsSes
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.exchanges as exc


#brk = Brokerservice()
abroker = Brokerservice() #setAuto=True)

user_email = "ben@enet.io" #os.environ["USER_EMAIL"]

abroker.set_apikeys_fromfile(user_id="ben")
abroker.activate_session(user_id="ben")

abroker.set_client(exc.DELTA)
client = abroker.get_client(exc.DELTA)
print (client)

prd = client.get_products()
print ("products ",prd)


"""

brk.activate_session(user_email)
brk.set_client(exc.DELTA)
delta_client = brk.get_client(exc.DELTA)

def calc_cum(orders, amount):
    z = 0
    i = 0    
    #print (len(orders))
    while z < amount and i<len(orders):
        o = orders[i]
        z += o['size']
        p = float(o['price'])
        #print (p)
        i+=1
    return p

def show_book(product, depth):
    book = delta_client.get_L2_orders(product)
    bids = book["buy_book"]
    asks = book["sell_book"]
    topbid = bids[0]
    topask = asks[0]
    tb = float(topbid['price'])
    ta = float(topask['price'])

    bid_point = calc_cum(bids,depth)
    ask_point = calc_cum(asks,depth)
    spread_amount = (ask_point - bid_point)/ask_point
    #print (bid_point,ask_point,spread_amount)
    
    #spread = (ta-tb)/tb
    #infostr = "bid %5.2f ask %5.2f  spread %3.2f%%"%(tb, ta, spread*100)
    infostr = "%3.2f%%"%(spread_amount*100)
    return infostr


depth = 1000
print ("symbol id  spread%, depth: ", depth)
for p in prd[:]:
    pid = p["id"]
    info = show_book(pid, depth)
    print (p["symbol"],p["id"],info)
"""