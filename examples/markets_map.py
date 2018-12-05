import archon.exchange.exchanges as exc
import archon.arch as arch
import archon.feeds.cryptocompare as cryptocompare
import pickle

a = arch.Arch()
a.set_keys_exchange_file()

ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.HITBTC, exc.BINANCE]
a.set_active_exchanges(ae)

#markets = a.fetch_global_markets()
#pickle.dump( markets, open( "markets.p", "wb" ) )
markets = pickle.load( open( "markets.p", "rb" ) )

def lowest_ask(v):
    la = 10**6
    for z in v:
        b,a = z['bid'],z['ask']
        if a < la: la = a
    return a

def highest_bid(v):
    hb = 0
    for z in v:
        b,a = z['bid'],z['ask']
        if b > hb: hb = b
    return hb


#market map by pair
market_map = dict()
for x in markets:
    p = x['pair']
    e = x['exchange']
    if p not in market_map:
        market_map[p] = [x]
    else:
        market_map[p].append(x)


for k,v in market_map.items():
    if len(v) > 4:        
        la = lowest_ask(v)
        hb = highest_bid(v)
        print ("** %s ** "%k)
        print (hb," ",la)
        for z in v:
            b,a = z['bid'],z['ask']
            e = z['exchange']            
            print (e,b,a)
            