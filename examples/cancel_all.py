""" 
cancel all
"""

import archon.broker as broker
import archon.exchange.exchanges as exc
from util import *

a = broker.Broker()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC,exc.BINANCE]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def cancel_all():
    a.cancel_all()

if __name__=='__main__': 
    cancel_all()
