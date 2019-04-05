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

if __name__ == '__main__':

    api_key = apikey
    seceret_key = secret
    passphrase = password

    accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, True)
    result = accountAPI.get_currencies()
    print (result)

    spotapi = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    result = spotapi.get_account_info()
    print (result)