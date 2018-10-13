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
ms = a.global_markets()

exs = list(set([x['exchange'] for x in ms]))
for e in exs:
    z = list(filter(lambda t: t['exchange']==e, ms))
    print (e,len(z))

for m in ms[:100]:
    if m['denom']=='BTC':
        print (m)
        