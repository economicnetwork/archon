import archon.feeds.coingecko as cg

api = cg.CoinGeckoAPI()

exc = api.get_exchanges_list()
for x in exc: 
    #v = x["trade_volume_24h_btc"]
    v = x["trade_volume_24h_btc_normalized"]
    if v > 5000:
        print (x["name"],v)