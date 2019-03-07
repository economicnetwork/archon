import requests
import json
from archon.exchange.delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size
 
delta_client = DeltaRestClient(
    #base_url='https://testnet-api.delta.exchange',
    #base_url=,
    api_key='',
    api_secret=''
)

def show_products():
    prd = delta_client.get_products()

    print ("...")
    for p in prd:
        print (p)
        print (p["symbol"],p["id"])

btc_Id = 9 #"BTCUSD_29Mar"
book = delta_client.get_L2_orders(btc_Id)
bids, asks = book["buy_book"], book["sell_book"]
print ("bid ", bids[0])
print ("ask ", asks[0])
#print (book.keys())
