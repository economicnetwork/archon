"""
show orderbooks for all exchanges
"""

import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as model
from archon.util import *

import time
import datetime
import math

abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file(exchanges=[exc.KRAKEN])
client = abroker.afacade.get_client(exc.KRAKEN)
market = model.market_from("BTC","USD")
smarket = model.conv_markets_to(market, exc.KRAKEN)   
b = client.get_balance()
print (b)
