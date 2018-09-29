import sys
sys.path.append('/Users/ben/archon')
import archon.broker as broker
import archon.arch as arch
import archon.exchange.exchanges as exc
import time
import datetime

from archon.util import *
from util import *
#from order_utils import *

import math

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
s_exchange = exc.CRYPTOPIA
abroker.set_singleton_exchange(s_exchange)

def user_tx():
    #db.user_txs.find()
    txs = abroker.get_tradehistory_all()
    for tx in txs[:]:
        ts = tx['TimeStamp'][:19]
        timestamp_from = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')        
        tx["timestamp"] = timestamp_from
        m = tx['Market']        
        tday = tx["timestamp"].day        
        if tday==27:
            r = tx['Rate']
            a = tx['Amount']
            ty = tx['Type']
            print (m,r,a,ty)
     
if __name__=='__main__':
    user_tx()