"""
https://github.com/bitkub/bitkub-official-api-docs
"""

import requests
import json

baseURL = "https://api.bitkub.com"

class Client:

    def __init__(self):
        pass

    def servertime(self):
        url = baseURL + "/api/servertime"
        result = requests.get(url).content
        return result

    def ticker(self):
        url = baseURL + "/api/market/ticker"
        result = requests.get(url).content
        result = json.loads(result)
        return result


    def bids(self):
        url = baseURL + "/api/market/bids"
        payload = {"sym": "BTC", "lmt": 100}
        result = requests.get(url, params=payload).content
        return result

if __name__=='__main__':
    c = Client()
    print (c.servertime())
    #print (c.bids())
    t = c.ticker()
    for k,v in t.items():
        print (k,v["last"])
