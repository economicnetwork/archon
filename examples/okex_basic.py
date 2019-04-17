import json

import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
from archon.broker.config import get_keys
import archon.exchange.okex.account_api as account
import archon.exchange.okex.ett_api as ett
import archon.exchange.okex.futures_api as future
import archon.exchange.okex.lever_api as lever
import archon.exchange.okex.spot_api as spot
import archon.exchange.okex.swap_api as swap


keys = get_keys(exc.OKEX)

apikey = keys["public_key"]
secret = keys["secret"]
password = keys["password"]

def get_market(target):
    market_list = list()
    t = spotapi.get_ticker()
    for x in t:
        s = x["instrument_id"]
        ac,dc = s.split('-')
        v = int(float(x["quote_volume_24h"]))
        #print (ac,dc,v)
        if dc == target:
            market_list.append([ac,dc,v])
    return market_list


if __name__ == '__main__':

    api_key = apikey
    seceret_key = secret
    passphrase = password

    accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, True)
    currencies = accountAPI.get_currencies()
    
    #for x in currencies:
    #    print (x)

    spotapi = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    result = spotapi.get_account_info()
    prices = {"BTC": 5000, "USDT": 1, "ETH": 160}
    for underlying in ["BTC", "USDT", "ETH"]:
        market_list = get_market(underlying)
        sumv = 0
        for x in market_list:
            #print (x)
            price = prices[underlying]
            sumv += x[2]* price
        print (underlying, " ", sumv)
