import logging
import os
import time

import numpy
from pymongo import MongoClient
#import archon.orders as orders
import archon.broker as broker
import archon.exchange.exchanges as exc
from archon.exchange.bitmex.fields import *
import archon.model.models as m

from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as mex
import time

abroker = Brokerservice()
user_email = "ben@enet.io"

abroker.set_apikeys_fromfile(user_id="ben")
abroker.activate_session(user_id="ben")

abroker.set_client(exc.BITMEX)
client = abroker.get_client(exc.BITMEX)

def show_desc(pos):    
    #print (pos['currentQty'])
    for k,v in pos.items():
        try:
            print (k,v," ",position_description[k])
        except:
            print ("...",k," ",v, " (no description)")

def show():
    #show_desc()
    pos = client.position()
    print ("pos ",pos)
    if pos: 
        pos = pos[0]
        unrelasedpnl = pos['unrealisedPnl']
        avgentry = pos['avgEntryPrice']
        #realisedpnl = pos['realisedPnl']
        #markprice = pos['markPrice']
        curQty = pos['currentQty']
        print ("unrelasedpnl, avgentry,markprice")
        print (unrelasedpnl, avgentry,curQty)
        #print (pos)            


if __name__ == '__main__': 
    print ("show balance")    
    #while True:
    show()