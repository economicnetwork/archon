
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
