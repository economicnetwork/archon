
import archon.model.models as m
import archon.exchange.exchanges as exc

def get_book(abroker):
    market = m.market_from("XBT","USD")   
    smarket = m.conv_markets_to(market, exc.BITMEX) 
    book = abroker.afacade.get_orderbook(smarket, exc.BITMEX)
    return book

def ob_ratio(book):
    """ ratio of top bid to top ask """
    bids,asks = book['bids'],book['asks']
    level = 0
    bq = bids[level]['quantity']
    aq = asks[level]['quantity']
    r = (bq/aq)
    return r

def ob_ratio_all(book):
    """ ratio of bid to ask """
    [bids,asks] = book['bids'],book['asks']
    tbq = 0
    taq = 0
    for level in range(0,len(bids)):
        #level = 0
        bq = bids[level]['quantity']
        aq = asks[level]['quantity']
        tbq +=bq 
        taq +=aq
    r = (tbq/taq)
    return r    

def mid_price(book):
    """ ratio of top bid to top ask """
    bids,asks = book['bids'],book['asks']
    #asks.reverse()
    level = 0
    bp = bids[level]['price']
    ap = asks[level]['price']
    mid = (bp+ap)/2
    return mid

def weighted_mid_price(book):
    """ weighted mid """
    bids,asks = book['bids'],book['asks']
    #asks.reverse()
    level = 0
    bp = bids[level]['price']
    ap = asks[level]['price']
    bq = bids[level]['price']
    aq = asks[level]['price']
    tq = bq + aq
    bf = bq/tq
    af = aq/tq
    wmid = bp * bf + ap * af
    return wmid    

def best_bid_price(book):
    bids = book['bids']
    bp = bids[0]['price']
    return bp

def best_ask_price(book):
    asks = book['asks']
    ap = asks[0]['price']
    return ap

def order_dict(order):
    #side,price = order['side'],order['price']
    selectkeys = ['side','price','symbol','leavesQty','simpleCumQty','cumQty','timestamp']
    o = {k: v for k, v in order.items() if k in selectkeys}    
    return o

def display_book(book,name="orderbook"):
    bids,asks = book['bids'],book['asks']
    #TODO bitmex
    #asks.reverse()
    print ("** bid **       %s     ** ask **"%(name))
    i = 0
    for b in bids[:10]:
        ask = asks[i]  
        bp = b['price']
        ap = ask['price']
        av = ask['quantity']
        bv = b['quantity']
        print ("%.2f  %.0f   %.2f  %.0f" % (bp,bv,ap,av))
        i+=1
