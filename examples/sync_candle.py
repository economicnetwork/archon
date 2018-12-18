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
import pymongo

afacade = facade.Facade()
arch.setClientsFromFile(afacade)
a = arch.Arch()
#a.sync_candles_all("LTC_BTC")

db = a.get_db()

l = db.candles.find_one({"exchange":"Kucoin"})
for x in l['candles']:
    print (x)
