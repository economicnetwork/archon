
import logging
import os
import time

import numpy
from pymongo import MongoClient
import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as m


abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

def mid_price(book):
    """ ratio of top bid to top ask """
    bids,asks = book['bids'],book['asks']
    #asks.reverse()
    level = 0
    bp = bids[level]['price']
    ap = asks[level]['price']
    mid = (bp+ap)/2
    return mid

def get_book():
    market = m.market_from("XBT","USD")   
    smarket = m.conv_markets_to(market, exc.BITMEX) 
    book = abroker.afacade.get_orderbook(smarket, exc.BITMEX)
    return book
    
def submit_buy():
    book = get_book()
    mid = mid_price(book)
    #display_book(book)
    #print (mid)
    print (book)
    ttype = orders.ORDER_SIDE_BUY
    p = 0.01
    order_price = round(mid * (1 - p),0)
    qty = 1
    market = m.market_from("XBT","USD")
    order = [market,ttype,order_price,qty]
    result = abroker.submit_order(order, exc.BITMEX)
    print ("result ",result)

    oo = abroker.afacade.open_orders(exc.BITMEX)
    print (oo)

if __name__=='__main__':
    submit_buy()
"""    
print ("no open orders ")
display_book(book)
ttype = orders.ORDER_SIDE_SELL
p = 0.0001
order_price = round(mid * (1 + p),0)
qty = pqty
market = m.market_from("XBT","USD")
order = [market,ttype,order_price,qty]
print ("submit ",order)
result = abroker.submit_order(order, exc.BITMEX)
print ("result ",result)
"""