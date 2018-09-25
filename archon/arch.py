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

def setClientsFromFile(abroker):
    apikeys = apikeys_config()["apikeys"]     
        
    ck = apikeys["CRYPTOPIA"]    
    
    abroker.set_api_keys(exc.CRYPTOPIA,ck["public_key"],ck["secret"])
    #abroker.set_singleton_exchange(broker.EXC_CRYPTOPIA)

    bk = apikeys["BITTREX"]        
    abroker.set_api_keys(exc.BITTREX,bk["public_key"],bk["secret"])
    #abroker.set_singleton_exchange(broker.EXC_BITTREX)

    bk = apikeys["KUCOIN"]        
    abroker.set_api_keys(exc.KUCOIN,bk["public_key"],bk["secret"])

    gconf = general_config()
    abroker.set_mail_config(gconf["apikey"], gconf["domain"])
    