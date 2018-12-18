"""
send balance report to email
"""

import sys

import archon.exchange.exchanges as exc
import archon.facade as facade
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

def sort_usd(d):
    d = sorted(d, key=lambda k: k['USDvalue'])
    d.reverse()   
    return d

def process(bl):
    newbl = list()    
    for x in bl:        
        if x['USDvalue'] > 1:
            x['USDvalue'] = round(x['USDvalue'],2)
            newbl.append(x)
    newbl = sort_usd(newbl)
    return newbl

def write_to_file(html):
    #print (total_all)
    date_broker_format = "%Y-%m-%d"
    from datetime import datetime
    ds = datetime.now().strftime("%Y%m%d")
    fn = '../../balance_report' + ds + '.html'
    with open(fn,'w') as f:
        f.write(html)

def per_exchange(bl, e):
    l = list(filter(lambda x: x['exchange']==e,bl))
    per_exchange = round(sum([float(x['USDvalue']) for x in l]),2)
    return per_exchange

def per_currency(bl, c):
    l = list(filter(lambda x: x['symbol']==c,bl))
    per = round(sum([float(x['USDvalue']) for x in l]),2)
    return per

def balance_report():
    bl = a.global_balances_usd()
    print (bl)

    bl = process(bl)
    
    total_all = 0

    for x in bl:
        total_all += x['USDvalue']

    total_all = round(total_all,2)

    exc = list(set([x['exchange'] for x in bl]))
    per = list()
    for e in exc:
        x = per_exchange(bl,e)
        per.append({"exchange": e,"USDvalue":x})

    per = sort_usd(per)

    syms = list(set([x['symbol'] for x in bl]))
    #print (syms)
    per_currency_list = list()
    for c in syms:
        #print (c)
        x = per_currency(bl,c)
        per_currency_list.append({"symbol": c,"USDvalue":x})

    per_currency_list = sort_usd(per_currency_list)
    print ("per currency ",per_currency_list)

    print ("total all ",total_all)
    loader = jinja2.FileSystemLoader('./balances.html')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('')
    html = template.render(balances=bl,per=per,total=total_all,per_currency=per_currency_list)
    write_to_file(html)
    #mail.send_mail_html(afacade, "Balance Report", html)

if __name__=='__main__':
    balance_report()
    