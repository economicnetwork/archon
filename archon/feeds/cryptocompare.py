import requests
import json

url ="https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=USD"


#TMP fix for kraken
extra_values = {'ZUSD': 1,'ZEUR': 1,'XXBT': 6700,'XLTC':0,'XXLM':0, 'BOXX': 0.18}
replace_syms = {'XXBT':'BTC'}


def fetch_usdprice(symbol):
    r = requests.get(url%symbol)
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


            