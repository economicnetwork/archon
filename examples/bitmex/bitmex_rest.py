from archon.exchange.bitmex import bitmex
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as m

abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file(keys_filename="bitmex.toml")
client = abroker.afacade.get_client(exc.BITMEX)

def get_trades():
    path = "trade"
    count = 100
    query = {
        'reverse': 'false',
        'start': 0,
        'count': count,
        #'filter': args.filter
    }

    data = client._query_bitmex(path=path, verb="GET", query=query, timeout=10)
    print (data)

def get_exes():
    count = 100  # max API will allow
    query = {
        'reverse': 'true',
        'start': 0,
        'count': count,
        #'filter': args.filter
    }

    txdata = client._query_bitmex(path="execution/tradeHistory", verb="GET", query=query, timeout=10)
    print (txdata)
    for x in txdata:
        print (type(x))

def get_book():    
    symbol = "XBTUSD"    
    inst = client.get_instrument(symbol)
    print (inst['bidPrice'])
    print (inst['askPrice'])

    book = client.market_depth(symbol,depth=3)
    sells = list(filter(lambda x: x['side']=='Sell',book))
    buys = list(filter(lambda x: x['side']=='Buy',book))
    print (buys[0],sells[0])

def display_book(book,name):
    [bids,asks] = book
    print ("** bid **       %s     ** ask **"%(name))
    i = 0
    for b in bids[:10]:
        ask = asks[i]  
        bp = b['price']
        ap = ask['price']
        av = ask['quantity']
        bv = b['quantity']
        print ("%.8f  %.2f   %.8f  %.2f" % (bp,bv,ap,av))
        i+=1  

#get_book()
#market = "XBT-USD"    
market = m.market_from("XBT","USD")
book = abroker.afacade.get_orderbook(market, exc.BITMEX)
#print (book)
display_book(book,"BITMEX")