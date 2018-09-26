
from coinmarketcap import CoinMarketCap

usd_values = {'BTC':6400,'LTC':58,'ETH':200, 'TOMO': 0.25, 'HAV': 0.07,'BTG':0.01,'USDT':1.0,'BNB':9}

def cmc_price(symbol):
    print (symbol)    
    market = CoinMarketCap()
    #resp = market.coin_price("eos")
    resp = market.coin_market_price(symbol)['data']
    prices = list()
    for x in resp:
        e = x['exchange']
        p = x['pair']
        denom = p.split('/')[1]
        if denom == "USD":
            #print (e,x['price']['price_usd'])
            prices.append(x['price'])
    return prices[0]['price_usd']

def get_usd(symbol):
    if symbol not in usd_values:
        usd_price = cmc_price(symbol.lower())
        return usd_price
    else:
        return usd_values[symbol]

def unify_balance(binance_b):
    newl = list()
    for x in binance_b:
        s = x['asset']
        f = float(x['free'])
        l = float(x['locked'])        
        if f+l > 0:
            usd_price = get_usd(s)    
            d = {}
            d['symbol'] = s
            d['exchange'] = "Binance"            
            d['total'] = f+l
            d['USD-value'] = (f+l)*usd_price
            newl.append(d)
    return newl