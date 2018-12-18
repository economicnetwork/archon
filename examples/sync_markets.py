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
#a.sync_markets_all()

db = a.get_db()
l = list(db.markets.find({'denom':'BTC','volume':{'$gte':10}}).sort('volume',pymongo.DESCENDING))
for x in l:
    print (x['pair'],x['volume'],x['last'],x['high'],x['exchange'])

print (len(l))