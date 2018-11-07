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

client = abroker.get_client(exc.BINANCE)

ae = [exc.BINANCE]
a.set_active_exchanges(ae)

ms = a.fetch_global_markets()

ms = list(filter(lambda x: x['denom'] == 'BTC', ms))
print (len(ms))

for x in ms[:2]:
    print (x)
