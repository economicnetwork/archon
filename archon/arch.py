
import toml
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.markets as markets
import time
from archon.model import models
from archon.util import *
from pymongo import MongoClient
import datetime

logpath = './log'
log = setup_logger(logpath, 'archon_logger', 'archon')

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def apikeys_config(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def general_config(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def set_keys_exchange(abroker, e, keys):
    pubkey = keys["public_key"]
    secret = keys["secret"]
    abroker.set_api_keys(e,pubkey,secret)


def setClientsFromFile(abroker,keys_filename="apikeys.toml"):
    apikeys = apikeys_config(keys_filename)["apikeys"]     
        
    for k,v in apikeys.items():
        eid = exc.get_id(k)
        if eid >= 0:
            set_keys_exchange(abroker, eid, apikeys[k])
        else:
            print ("exchange not supported")


    gconf = general_config("conf.toml")["MAILGUN"]
    abroker.set_mail_config(gconf["apikey"], gconf["domain"],gconf["email_from"],gconf["email_to"])

    
    

class Arch:
    """ 
    communitates with broker
    keeps datastructures in memory
    """

    def __init__(self):
        filename = "apikeys.toml"
        self.abroker = broker.Broker()
        setClientsFromFile(self.abroker, filename)
        #in memory data
        self.balances = None
        self.openorders = list()
        self.submitted_orders = list()
        self.active_exchanges = None
        e = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA] #, exc.HITBTC]
        self.set_active_exchanges(e)
        self.selected_exchange = None

        mongo_conf = general_config("conf.toml")["MONGO"]
        #mongoHost = mongo_conf['host']
        dbName = mongo_conf['db']        
        url = mongo_conf["url"]
        self.set_mongo(url, dbName)
        

    def set_mongo(self, url, dbName):
        #self.mongoHost = mongoHost
        #self.mongoPort = mongoPort
        self.mongo_url = url
        log.info("using mongo " + str(url))
        self.mongoclient = MongoClient(self.mongo_url)
        self.db = self.mongoclient[dbName]

    def get_db(self):
        return self.db

    def set_active_exchange(self, exchange):
        self.selected_exchange = exchange

    def set_active_exchanges(self, exchanges):
        self.active_exchanges = exchanges        

    def sync_orders(self):
        #TODO compare status of submitted_orders
        self.openorders = self.abroker.all_open_orders(self.active_exchanges)

    def get_by_id(self, oid):
        x = list(filter(lambda x: x['oid'] == oid, self.openorders))
        return x[0]

    def submit_order(self, order, exchange=None):
        if exchange is None: exchange=self.selected_exchange
        #TODO check balance before submit
        market,ttype,order_price,qty = order
        self.submitted_orders.append(order)
        self.abroker.submit_order(order, exchange)

    def cancel_order(self, oid):                
        order = self.get_by_id(oid)
        #oid, otype=None,exchange=None,symbol=None):
        oid, otype,exchange, market = order['oid'],order['otype'],order['exchange'],order['market']
        exchange = exc.get_id(exchange)
        self.abroker.cancel_id(oid, otype, market, exchange)

    def cancel_all(self, exchange=None):
        #log.info("cancel all")
        if exchange is None: exchange=self.selected_exchange
        self.sync_orders()
        for o in self.openorders:
            log.info("cancel " + str(o))
            self.cancel_order(o['oid'])
        
    def global_markets(self):
        allmarkets = list()
        for e in self.active_exchanges:
            n = exc.NAMES[e]
            log.info("fetch %s"%n)
            m = self.abroker.get_market_summaries(e)
            allmarkets += m
        return allmarkets

    def filter_markets(self, m):
        f = lambda x: markets.is_btc(x['pair'])
        m = list(filter(f, m))
        return m

    def sync_orderbook(self, market, exchange):
        smarket = models.conv_markets_to(market, exchange)  
        #print ("sync",market," ",exchange)   
        #TODO check if symbol is supported by exchange   
        try:
            n = exc.NAMES[exchange]
            [bids,asks] = self.abroker.get_orderbook(smarket,exchange)
            dt = datetime.datetime.utcnow()
            x = {'market': market, 'exchange': n, 'bids':bids,'asks':asks,'timestamp':dt}
            
            self.db.orderbooks.remove({'market':market,'exchange':exchange})
            self.db.orderbooks.insert(x)
            self.db.orderbooks_history.insert(x)
        except:
            print ("symbol not supported")

    def sync_orderbook_all(self, market):        
        for e in self.active_exchanges:            
            self.sync_orderbook(market, e)   

    def sync_tx(self, market, exchange):
        #print ("sync",market," ",exchange)   
        try:            
            smarket = models.conv_markets_to(market, exchange)  
            txs = self.abroker.market_history(smarket,exchange)
            n = exc.NAMES[exchange]
            smarket = models.conv_markets_to(market, exchange)
            dt = datetime.datetime.utcnow()
            x = {'market': market, 'exchange': n, 'tx':txs,'timestamp':dt}
            self.db.txs.remove({'market':market,'exchange':n})
            self.db.txs.insert(x)     
            self.db.txs_history.insert(x)
        except:
            print ("symbol not supported")

    def sync_tx_all(self, market):              
        for e in self.active_exchanges:
            self.db.txs.remove({'market':market,'exchange':e})
            self.sync_tx(market, e)   

    def sync_markets(self, exchange):
        self.db.markets.drop()
        ms = self.global_markets()

        dt = datetime.datetime.utcnow()
        #print ("got markets %i"%(len(ms)))
        #db.markets.insert({'markets':ms,'timestamp':dt})
        for x in ms:
            x['timestamp'] = dt
            n,d = x['pair'].split('_')
            x['nom'] = n
            x['denom'] = d
            self.db.markets.insert(x)
        



