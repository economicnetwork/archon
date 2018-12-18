"""
balances simple
"""

import archon.broker as broker

a = broker.Broker()
a.set_keys_exchange_file()

bl = a.global_balances()
print (bl)
