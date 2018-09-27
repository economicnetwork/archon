
#from coinmarketcap import CoinMarketCap
import archon.exchange.exchanges as exc

#TODO make dynamic
#usd_values = {'BTC':6400,'LTC':58,'ETH':200, 'TOMO': 0.25, 'HAV': 0.07,'BTG':0.01,'USDT':1.0,'BNB':9,'ADA':0.1,'ARK':0,'BCH':0,'XRP':0.2,'BOXX':0.15}
#usd_values = {'BTC':6400,'LTC':58,'ETH':200, 'TOMO': 0.25, 'HAV': 0.07,'BTG':0.01,'USDT':1.0,'BNB':9,'XRP':0.5,'BOXX':0.15,'EMC2':0,'ZCL':0.1,'ADA':0.1,'ARK':0,'BCH':0}
extra_values = {'BOXX':0.15,'ZUSD': 1, 'ZEUR': 1, 'XXBT': 6500,'XLTC':0,'XXLM':0,'USDT':1,'DASH':0,'BCH':0}

def compare_price(symbol):
    r = requests.get(url%symbol)
    j = json.loads(r.content)
    return j['USD']

def get_usd(symbol):
    if symbol in extra_values.keys():
        return extra_values[symbol]
    else:
        try:
            return compare_price(symbol)
        except:
            return 0

def unify_balance(b,exchange):

    if exchange==exc.CRYPTOPIA:
        newl = list()
        for x in b:
            d = {}
            s = x['Symbol']
            d['symbol'] = s            
            t = float(x['Total'])
            if t > 0:
                usd_price = get_usd(s)                
                #print (usd_price,t)
                d['total'] = t
                #d['USD-value'] = t*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.BITTREX:
        newl = list()
        for x in b:
            d = {}
            s = x['Currency']
            d['symbol'] = s
            t = float(x['Balance'])
            if t > 0:
                usd_price = get_usd(s)                
                d['total'] = t
                #d['USD-value'] = t*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.BINANCE:    
        newl = list()
        for x in b:
            s = x['asset']
            f = float(x['free'])
            l = float(x['locked'])        
            if f+l > 0:
                
                d = {}
                d['symbol'] = s
                d['exchange'] = "Binance"            
                d['total'] = f+l
                #usd_price = get_usd(s)    
                #d['USD-value'] = (f+l)*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.KUCOIN:
        newl = list()
        for x in b:
            s = x['coinType']            
            bb = x['balance']
            if bb > 0:
                
                d = {}            
                d['symbol'] = s
                d['exchange'] = "Kucoin"            
                d['total'] = bb
                #usd_price = get_usd(s)    
                #d['USD-value'] = bb*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.KRAKEN:
        newl = list()
        for k,v in b.items():
            d = {}
            d['symbol'] = k
            d['total'] = v
            newl.append(d)  
        return newl