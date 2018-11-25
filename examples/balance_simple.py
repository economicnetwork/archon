"""
send balance report to email
"""

import sys

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.plugins.mail as mail

import json
import requests
from jinja2 import Template
import jinja2
import pickle

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

def balance_report():
    bl = a.global_balances()
    print (bl)

if __name__=='__main__':
    balance_report()
    