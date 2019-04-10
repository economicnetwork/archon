#export COINMARKETCAP_APIKEY=''

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import os

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
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

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)["data"]
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

