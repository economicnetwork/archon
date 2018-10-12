
import toml
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.markets as markets
import time
from archon.util import *

logpath = './log'
log = setup_logger(logpath, 'archon_logger', 'archon')

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def apikeys_config(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def general_config():
    toml_string = toml_file("conf.toml")
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


    gconf = general_config()["MAILGUN"]
    abroker.set_mail_config(gconf["apikey"], gconf["domain"],gconf["email_from"],gconf["email_to"])

    mongo_conf = general_config()["MONGO"]
    #mongoHost = mongo_conf['host']
    dbName = mongo_conf['db']        
    url = mongo_conf["url"]
    abroker.set_mongo(url, dbName)
    

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
        e = [exc.KUCOIN, exc.BITTREX, exc.CRYPTOPIA, exc.HITBTC]
        self.set_active_exchanges(e)
        self.selected_exchange = None

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
        for e in [exc.CRYPTOPIA,exc.BITTREX,exc.KUCOIN,exc.HITBTC]:
        #for e in [exc.HITBTC]:
            n = exc.NAMES[e]
            log.info("fetch %s"%n)
            m = self.abroker.get_market_summaries(e)
            allmarkets += m
        return allmarkets

    def filter_markets(self, m):
        f = lambda x: markets.is_btc(x['pair'])
        m = list(filter(f, m))
        return m
