import archon.feeds.coingecko as cg

api = cg.CoinGeckoAPI()

def get_coin_list():
    coins = api.get_coins_list()

    print ("number of coins ", len(coins))

    for x in coins[:1]:
        print(x["id"],x.keys())

    markets = api.get_coins_markets(vs_currency="usd")
    for x in markets:
        print (x)
        #print (x["id"],x["current_price"])

    print (len(markets))

coin_info = api.get_coins()
for x in coin_info[:10]:
    print (x.keys())