"""
binance tickers
"""

import archon.broker.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(path_file_apikeys="./apikeys.toml")
#a.afacade.set_api_keys(exc.BINANCE, pub, priv)
client = a.afacade.get_client(exc.BINANCE)
t = client.get_all_tickers()

for x in t[:1]:
    print (x)