import requests
import json

baseURL = "https://min-api.cryptocompare.com/data/"
priceurl = baseURL + "price"
#?fsym=%s&tsyms=USD"






#TMP fix for kraken
extra_values = {'ZUSD': 1,'ZEUR': 1,'XXBT': 6700,'XLTC':0,'XXLM':0, 'BOXX': 0.18}
replace_syms = {'XXBT':'BTC'}


def fetch_usdprice(symbol):
    r = requests.get(priceurl%symbol)
    j = json.loads(r.content)
    return j['USD']

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
    resolution=60
    histurl = baseURL + "histoday"
    #/data/histohour' : '/data/histominute'
    # "BitTrex" #"Bitfinex"    
    #e = "Bitfinex"
    fromt=1534847201
    tot=1540031261
    first=True 
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
