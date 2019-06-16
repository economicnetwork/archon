"""
balances simple
"""

import archon.broker.broker as broker
import archon.exchange.exchanges as exc


"""
a = broker.Broker()
a.set_active_exchanges([exc.BINANCE])
bl = a.global_balances()
print (bl)
for x in bl: 
	for k,v in x.items(): 
		print (k,":",v)
"""

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(path_file_apikeys="./apikeys.toml")
client = a.afacade.get_client(exc.BINANCE)
print (client.get_account())