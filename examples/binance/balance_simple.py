"""
balances simple
"""

import archon.broker.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(path_file_apikeys="./apikeys.toml")
client = a.afacade.get_client(exc.BINANCE)
bal = client.get_account()["balances"]
for x in bal:
	f,l = float(x["free"]),float(x["locked"])
	a = x["asset"]
	total = f+l
	if total > 0:
		print (a,total)