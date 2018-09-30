""" unified model """

import archon.exchange.exchanges as exc
import archon.tx as atx
import datetime

# ---- key names ----

def price_key(exchange):
    if exchange==exc.CRYPTOPIA:
        price_key = "Price"
        return price_key
    elif exchange==exc.BITTREX:
        price_key = "Rate"
        return price_key

def qty_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Volume"
        return key
    elif exchange==exc.BITTREX:
        return "Quantity"

def o_key_price(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Rate"
    elif exchange==exc.BITTREX:
        return "Limit"

def o_key_id(exchange):
    if exchange==exc.CRYPTOPIA:
        return "OrderId"
    elif exchange==exc.BITTREX:
        return "OrderUuid"

def otype_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Type"
    elif exchange==exc.BITTREX:
        return "OrderType"

def otype_key_buy(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Buy"
    elif exchange==exc.BITTREX:
        return "LIMIT_BUY"

def otype_key_sell(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Sell"
    elif exchange==exc.BITTREX:
        return "LIMIT_SELL"

def tx_amount_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Amount"

def book_key_qty(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Volume"
        return key
    elif exchange==exc.BITTREX:
        return "Quantity"

def book_key_price(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Price"
        return key
    elif exchange==exc.BITTREX:
        return "Rate"

def bid_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "BidPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Bid"        

def ask_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "AskPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Ask"

def conv_usertx(tx, exchange):
    if exchange==exc.CRYPTOPIA:
        r = tx['Rate']
        a = tx['Amount']
        ty = tx['Type']
        m = tx['Market']
        ts = tx['TimeStamp'][:19]
        dt = atx.conv_timestamp_tx(ts,exchange)
        d = {'price':r,'quantity':a,'txtype':ty,'market':m,'timestamp':dt}
        return d

    elif exchange==exc.BITTREX:
        t = tx['TimeStamp']
        #2018-09-10T17:07:44.507
        dt = atx.conv_timestamp(t,exchange)
        p = tx['Limit']
        q = tx['Quantity']
        d = {'price':p,'quantity':q,'timestamp':dt} #,'txtype':ty,'market':m,'timestamp':timestamp_from}
        return d

def conv_orderbook(book, exchange):
    if exchange==exc.CRYPTOPIA:
        bids = (book["Buy"])
        asks = (book["Sell"])
        rate_key = book_key_price(exchange)
        qty_key =  book_key_qty(exchange)
        newb = list()
        for b in bids:
            newb.append({'price':b[rate_key],'quantity':b[qty_key]})
        newa = list()
        for a in asks:
            newa.append({'price':a[rate_key],'quantity':a[qty_key]})            
        return [newb,newa]
    elif exchange==exc.BITTREX:
        bids = book["buy"]
        asks = book["sell"]
        rate_key = book_key_price(exchange)
        qty_key =  book_key_qty(exchange)
        newb = list()
        for b in bids:
            newb.append({'price':b[rate_key],'quantity':b[qty_key]})
        newa = list()
        for a in asks:
            newa.append({'price':a[rate_key],'quantity':a[qty_key]})            
        return [newb,newa]
    elif exchange==exc.KUCOIN:
        bids = (book["BUY"])
        asks = (book["SELL"])
        newb = list()
        for b in bids:
            p,v,t = b
            d = {'price':p,'volume':v}
            newb.append(d)
        newa = list()
        for a in asks:
            p,v,t = b
            d = {'price':p,'volume':v}
            newa.append(d)
        book = [newb,newa]
        return book
