import requests
import json
from archon.exchange.delta.delta_rest_client import create_order_format, cancel_order_format, round_by_tick_size
from archon.exchange.delta.instruments import btc_march, btc_march_quanto, btc_june, product_names
import archon.exchange.exchanges as exc
from archon.plugins.aws_ses import AwsSes

from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.exchanges as exc

import os
brk = Brokerservice()
user_email = "ben"
#os.environ["USER_EMAIL"]
brk.activate_session(user_email)
brk.set_client(exc.DELTA)
delta_client = brk.get_client(exc.DELTA)

def show_book(product):
    book = delta_client.get_L2_orders(product)
    bids = book["buy_book"]
    asks = book["sell_book"]
    for a in asks[:5]:
        print (a)

    print ('******')
    for b in bids[:5]:
        print (b)

    topbid = bids[0]
    topask = asks[0]
    tb = float(topbid['price'])
    ta = float(topask['price'])
    spread = (ta-tb)/tb
    print (product, tb,ta, spread)
    product_name = product_names[product]
    infostr = "%s  :  bid %5.2f ask %5.2f  spread %6.5f"%(product_name, tb, ta, spread)
    return infostr

def send_mail_report(body):    
    awsses = AwsSes(user_email)
    headline = "Delta"
    html = """<html><head></head><body><h1>%s</h1><p>%s</p></body></html>"""%(headline, body)

    awsses.send_mail(user_email, html, "Delta price")

def show_products():
    p = delta_client.get_products()
    for x in p:        
        print (x["id"],x["description"],x["symbol"])

#all_info = ""
#all_info += show_book(btc_march) + "<br>"
#all_info += show_book(btc_june) + "<br>"
#all_info += show_book(btc_march_quanto) + "<br>"
#send_mail_report(all_info)
show_book()
