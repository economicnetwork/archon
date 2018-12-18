import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.arch as arch
import archon.markets as m
import archon.feeds.cryptocompare as cryptocompare
import json
import requests
import time
import datetime

a = arch.Arch()
a.set_keys_exchange_file()

client = a.afacade.get_client(exc.BINANCE)

ae = [exc.BINANCE]
a.set_active_exchanges(ae)

ms = a.fetch_global_markets()

ms = list(filter(lambda x: x['denom'] == 'BTC', ms))
print (len(ms))

for x in ms[:2]:
    print (x)
