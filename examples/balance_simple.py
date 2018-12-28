"""
balances simple
"""

import archon.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker()
a.set_active_exchanges([exc.BINANCE])
bl = a.global_balances()
print (bl)
