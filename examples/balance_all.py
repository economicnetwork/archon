"""
send balance report to email
"""

import sys
sys.path.append('/Users/ben/archon')

import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch
import archon.plugins.mail as mail

import json
import requests
from jinja2 import Template
import jinja2
import pickle

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

#TMP fix for kraken
extra_values = {'ZUSD': 1,'ZEUR': 1,'XXBT': 6700,'XLTC':0,'XXLM':0}


url ="https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=USD"

def compare_price(symbol):
    r = requests.get(url%symbol)
    j = json.loads(r.content)
    return j['USD']

def get_usd(symbol):
    if symbol in extra_values.keys():
        return extra_values[symbol]
    else:
        try:
            return compare_price(symbol)
        except:
            return 0

def process(bl):
    newbl = list()    
    for x in bl:
        x['USDvalue'] = round(x['USDvalue'],2)
        if x['USDvalue'] > 1:
            newbl.append(x)
    newbl = sorted(newbl, key=lambda k: k['USDvalue'])
    newbl.reverse()
    return newbl

def fetch_balances():

    bl = list()
    for e in [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.BINANCE,exc.KRAKEN]:
        b = abroker.balance_all(exchange=e)
        for x in b:
            n = exc.NAMES[e]
            x['exchange'] = n
            s = x['symbol']
            t = float(x['total'])
            if t > 0:
                #print ("total " + str(t))
                usd_price = get_usd(s)    
                x['USDprice'] = usd_price        
                x['USDvalue'] = round(t*usd_price,2)
                
                if x['USDvalue'] > 1:
                    bl.append(x)


    return bl

def write_to_file(html):
    #print (total_all)
    date_broker_format = "%Y-%m-%d"
    from datetime import datetime
    ds = datetime.now().strftime("%Y%m%d")
    with open('reports/balance_report' + ds + '.html','w') as f:
        f.write(html)

def balance_report():
    bl = fetch_balances()
    pickle.dump( bl, open( "balances.p", "wb" ) )
    #bl = pickle.load( open( "balances.p", "rb" ) )
    bl = process(bl)
    print (bl)

    total_all = 0

    for x in bl:
        total_all += x['USDvalue']

    total_all = round(total_all,2)

    loader = jinja2.FileSystemLoader('./balances.html')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('')
    html = template.render(balances=bl,total=total_all)
    #write_to_file(html)
    mail.send_mail_html(abroker, "Balance Report", html)

if __name__=='__main__':
    balance_report()
