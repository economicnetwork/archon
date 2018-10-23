import sys
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.markets as m
import archon.feeds.cryptocompare as cryptocompare
import json
import requests
import time
import datetime

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
a = arch.Arch()
a.sync_markets_all()
ms = a.get_markets()

print ("markets per exchange")
exs = list(set([x['exchange'] for x in ms]))
for e in exs:
    z = list(filter(lambda t: t['exchange']==e, ms))
    print (e,len(z))

"""
for m in ms[:10]:
    if m['denom']=='BTC':
        print (m)
"""