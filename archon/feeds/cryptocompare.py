import requests
import json

baseURL = "https://min-api.cryptocompare.com/data/"

usdprice_url = "https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=USD"

priceurl = baseURL + "price?fsym=%s&tsyms=USD"

#TMP fix for kraken
extra_values = {'ZUSD': 1,'ZEUR': 1,'XXBT': 6700,'XLTC':0,'XXLM':0, 'BOXX': 0.18}
replace_syms = {'XXBT':'BTC'}


def fetch_usdprice(symbol):
    url = priceurl%symbol
    r = requests.get(url)
    j = json.loads(r.content)
    usd = j['USD']
    return usd

def get_usd(symbol):
    #kraken fix, should be done by caller
    if symbol in replace_syms.keys():
        symbol = replace_syms[symbol]
    if symbol in extra_values.keys():
        return extra_values[symbol]
    else:
        try:
            return fetch_usdprice(symbol)
        except Exception as err:
            print (err)
            return 0

def get_hist(fsym, tsym, e):
    #"https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym + "&tsym=" + tsym + "&limit=500&e=CCCAGG";
    resolution=60
    histurl = baseURL + "histoday"
    #/data/histohour' : '/data/histominute'
    # "BitTrex" #"Bitfinex"    
    #e = "Bitfinex"
    limit=1000  
    payload = {'fsym': fsym, 'tsym': tsym, 'limit': limit,'e': e}
    payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
    histurl += "?" + payload_str
    print (histurl)
    r = requests.get(histurl)
    j = json.loads(r.content)
    with open('tv.json','w') as f:
        f.write(json.dumps(j))
    return j        
