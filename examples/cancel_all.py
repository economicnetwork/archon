""" 
cancel all
"""

import archon.arch as arch
import archon.exchange.exchanges as exc
from util import *

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def cancel_all():
    a.cancel_all()

if __name__=='__main__': 
    cancel_all()
