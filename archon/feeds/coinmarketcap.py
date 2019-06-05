#export COINMARKETCAP_APIKEY='aaaa'

"""
ENDPOINTS
Cryptocurrency	/v1/cryptocurrency/info	Get cryptocurrency metadata	https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id=1,2,10
Cryptocurrency	/v1/cryptocurrency/map	Get cryptocurrency CoinMarketCap ID map	https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?listing_status=active&start=1&limit=100
Cryptocurrency	/v1/cryptocurrency/listings/latest	List all cryptocurrencies (latest)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
Cryptocurrency	/v1/cryptocurrency/listings/historical	List all cryptocurrencies (historical)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?date=2018-10-10&sort=market_cap&start=1&limit=10&cryptocurrency_type=tokens&convert=USD,BTC

Cryptocurrency	/v1/cryptocurrency/market-pairs/latest	Get cryptocurrency market pairs (latest)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/market-pairs/latest?id=1&convert=LTC,ETH
Cryptocurrency	/v1/cryptocurrency/ohlcv/historical	Get cryptocurrency OHLCV values (historical)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?time_start=2017-01-01&id=1&time_start=2017-01-01&time_end=2018-01-
Cryptocurrency	/v1/cryptocurrency/ohlcv/latest	Get cryptocurrency OHLCV values (latest)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/latest?convert=CAD
Cryptocurrency	/v1/cryptocurrency/quotes/latest	Get cryptocurrency market quotes (latest)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,XRP,BCH,EOS,LTC,XLM&convert=BTC,ETH,EUR
Cryptocurrency	/v1/cryptocurrency/quotes/historical	Get cryptocurrency market quotes (historical)	https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical?id=1&time_start=2017&time_end=2018&interval=30d&count=12

Exchange	/v1/exchange/info	Get exchange metadata	https://pro-api.coinmarketcap.com/v1/exchange/info?id=1,2,10
Exchange	/v1/exchange/map	Get exchange to CoinMarketCap ID map	https://pro-api.coinmarketcap.com/v1/exchange/map?listing_status=active&start=1&limit=100
Exchange	/v1/exchange/listings/latest	List all exchanges (latest)	https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?limit=10&market_type=no_fees&convert=USD
Exchange	/v1/exchange/market-pairs/latest	Get exchange market pairs (latest)	https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=gdax&convert=LTC,XRP,EUR
Exchange	/v1/exchange/quotes/latest	Get exchange market quotes (latest)	https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?id=2,16&convert=USD,BTC,LTC,EUR
Exchange	/v1/exchange/quotes/historical	Get exchange market quotes (historical)	https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?id=270&time_start=2018-01-01&time_end=2018-05-01&interval=30d&count=12
Global Metrics	/v1/global-metrics/quotes/latest	Get aggregate market metrics (latest)	https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert=BTC,ETH,LTC,EUR
Global Metrics	/v1/global-metrics/quotes/historical	Get aggregate market metrics (historical)	https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical?interval=monthly&count=100
Tools	/v1/tools/price-conversion	Price conversion tool	https://pro-api.coinmarketcap.com/v1/tools/price-conversion?symbol=BTC&amount=50&convert=USD,GBP,LTC



map
{
"id": 1,
"name": "Bitcoin",
"symbol": "BTC",
"slug": "bitcoin",
"is_active": 1,
"first_historical_data": "2013-04-28T18:47:21.000Z",
"last_historical_data": "2019-04-05T20:44:01.000Z",
"platform": null
},

metadata
"1": {
"urls": {
"website": [
"https://bitcoin.org/"
],
"twitter": [ ],
"reddit": [
"https://reddit.com/r/bitcoin"
],
"message_board": [
"https://bitcointalk.org"
],
"announcement": [ ],
"chat": [ ],
"explorer": [
"https://blockchain.info/",
"https://live.blockcypher.com/btc/",
"https://blockchair.com/bitcoin"
],
"source_code": [
"https://github.com/bitcoin/"
]
},
"logo": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
"id": 1,
"name": "Bitcoin",
"symbol": "BTC",
"slug": "bitcoin",
"description": "Bitcoin (BTC) is a consensus network that enables a new payment system and a completely digital currency. Powered by its users, it is a peer to peer payment network that requires no central authority to operate. On October 31st, 2008, an individual or group of individuals operating under the pseudonym "Satoshi Nakamoto" published the Bitcoin Whitepaper and described it as: "a purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without going through a financial institution."",
"date_added": "2013-04-28T00:00:00.000Z",
"tags": [
"mineable"
],
"platform": null,
"category": "coin"
"""

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import os

base_url = 'https://pro-api.coinmarketcap.com/v1/'
cmc_key = os.environ["COINMARKETCAP_APIKEY"]

def get_listings(start=1,limit=1000):
    parameters = {
        'start': start,
        'limit': str(limit),
        'convert': 'USD',
        'sort': 'market_cap'
    }
    #sort=market_cap&start=1&limit=10&cryptocurrency_type=tokens&convert=USD,BTC
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

def get_listings_all():
    allcoins = list()
    for i in range(1,10000,1000):
        print ("get ",i)
        coins = get_listings(start=i)
        allcoins += coins
    return allcoins


def get_description(idlist):
    endpoint_description = "cryptocurrency/info"
    
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
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("error ", e)    

def get_description_all(maxr=10000):
    print ("get_description_all")
    allcoins = list()
    #maxr = 10000
    for x in range(1,maxr,100):
        #print (x)
        try:
            idlist = ','.join([str(z) for z in range(x,x+100)])
            print ("get ",x,idlist)
            coins = list(get_description(idlist).values())
            #print (coins)
            print ("result ",len(coins))
            #print (coins[0])
            allcoins += coins
            
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

