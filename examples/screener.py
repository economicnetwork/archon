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

a = arch.Arch()
a.set_keys_exchange_file()


ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.HITBTC, exc.BINANCE]
a.set_active_exchanges(ae)

ms = a.fetch_global_markets()
print (len(ms))

ms2 = list(filter(lambda x: x['denom'] == 'BTC', ms))
print (len(ms2))

ms = sorted(ms, key=lambda k: k['volume']) 

print ("simple screen sorted by volume\npair last")
for m in ms[:100]:
        if m['denom']!="BTC": continue
        print (m['pair'],m['last'])

