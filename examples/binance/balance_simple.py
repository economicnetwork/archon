"""
balances simple
"""

import archon.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker()
a.set_active_exchanges([exc.BINANCE])
bl = a.global_balances()
print (bl)
for x in bl: 
	for k,v in x.items(): 
		print (k,":",v)
