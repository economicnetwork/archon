"""
balances simple
"""

import archon.arch as arch

a = arch.Arch()
a.set_keys_exchange_file()

bl = a.global_balances()
print (bl)
