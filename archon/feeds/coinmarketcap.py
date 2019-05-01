#export COINMARKETCAP_APIKEY=''

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import os

base_url = 'https://pro-api.coinmarketcap.com/v1/'
cmc_key = os.environ["COINMARKETCAP_APIKEY"]

def get_summary():
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': 'USD',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_key,
    }

    session = Session()
    session.headers.update(headers)

    endpoint_summary = 'cryptocurrency/listings/latest'
    try:
        url = base_url + endpoint_summary
        response = session.get(url, params=parameters)
        data = json.loads(response.text)["data"]
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def get_description(start):
    endpoint_description = "cryptocurrency/info"
    idlist = ','.join([str(x) for x in range(start+1,start+100)])
    #[str(x)+',' for x in range(1,20)]
    parameters = {
        #'symbol': 'BTC,ETH,XRP,LTC'
        'id':idlist
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        url = base_url + endpoint_description
        response = session.get(url, params=parameters)
        data = json.loads(response.text)["data"]
        #print (data)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)    

def get_description_all():
    allcoins = list()
    for x in range(0,1000,100):
        try:
            print ("get ",x)
            coins = list(get_description(x).values())
            print (len(coins))
            print (coins[0])
            allcoins += coins
            import time
            time.sleep(1)
        except:
            pass
    return allcoins

def get_coin_map(active):
    endpoint_map = "cryptocurrency/map"    
    parameters = {
        'listing_status': active
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': cmc_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        url = base_url + endpoint_map
        response = session.get(url, params=parameters)
        data = json.loads(response.text)["data"]
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)        