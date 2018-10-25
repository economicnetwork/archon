"""
send balance report to email
"""

import sys

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.eventloop as eventloop
import archon.plugins.mail as mail

import json
import requests
from jinja2 import Template
import jinja2
import pickle

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
a = arch.Arch()
ae = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.KRAKEN, exc.BINANCE, exc.HITBTC]
a.set_active_exchanges(ae)

if __name__=='__main__':
    e = eventloop.Eventloop(abroker)
    e.start()
    e.join()
    