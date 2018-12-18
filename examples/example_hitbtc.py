import sys
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker
import archon.plugins.mail as mail

import json
import requests
from jinja2 import Template
import jinja2
import pickle

afacade = facade.Facade()
broker.setClientsFromFile(afacade)

client = afacade.get_client(exc.HITBTC)
#print (client)
#print (client.get_currenices())
"""
ab = client.get_account_balance()
for x in ab:
    av = float(x['available'])
    r = float(x['reserved'])
    if av+r > 0:
        print (x)

tb = client.get_trading_balance()        
for x in tb:
    av = float(x['available'])
    r = float(x['reserved'])
    if av+r > 0:
        print (x)

b = afacade.balance_all(exc.HITBTC)
print (b)
"""
t = client.get_tickers()
print (t)