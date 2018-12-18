import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker
import archon.markets as m
import archon.feeds.cryptocompare as cryptocompare
import json
import requests
import time
import datetime
import pymongo

afacade = facade.Facade()
broker.setClientsFromFile(afacade)
a = broker.Broker()
#a.sync_candles_all("LTC_BTC")

db = a.get_db()

l = db.candles.find_one({"exchange":"Kucoin"})
for x in l['candles']:
    print (x)
