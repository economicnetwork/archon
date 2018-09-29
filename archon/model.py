""" unified model """

import archon.exchange.exchanges as exc

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
        key = "Bid"
        return key
    elif exchange==exc.BITTREX:
        return "BidPrice"        

def ask_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Ask"
        return key
    elif exchange==exc.BITTREX:
        return "AskPrice"  