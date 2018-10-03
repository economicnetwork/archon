from pymongo import MongoClient
import os
from datetime import datetime

#export MONGO_URL=mongodb://localhost:27017/mxn

try:
    host = os.environ['MONGO_URL']
except:
    host = 'localhost' 

try:
    port = os.environ['MONGODB_PORT_27017_TCP_PORT']
except:
    port = 27017

#host = 'localhost'
print ("connecting mongo host %s %i" % (str(host),port))

client = MongoClient(host, port)
db = client.archon

def db_count_report(log):
    d = {"orderbook":db.orderbooks, "balance": db.balance, "balance history": db.balance_history, \
         "openorders": db.openorders, "openorders_history": db.openorders_history}

    log.info("** data base report **")
    for k,v in d.items():
        log.info("%s %s"%(k,v.find().count()))

def insert_balance(b):    
    ds = datetime.now().strftime("%Y%m%d")
    b["timestamp"] = ds
    db.balances.insert(b)
