from archon.exchange.bitmex import bitmex
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(keys_filename="bitmex.toml")
client = a.afacade.get_client(exc.BITMEX)

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

get_book()