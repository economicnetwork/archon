""" 
arch
"""

import toml
import archon.broker as broker
import archon.exchange.exchanges as exc
import time
from archon.util import *

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def apikeys_config():
    toml_string = toml_file("apikeys.toml")
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def general_config():
    toml_string = toml_file("conf.toml")
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def set_keys_exchange(abroker, e,keys):
    pubkey = keys["public_key"]
    secret = keys["secret"]
    abroker.set_api_keys(e,pubkey,secret)


def setClientsFromFile(abroker):
    apikeys = apikeys_config()["apikeys"]     
        
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
    
