""" 
arch
"""

import toml
import broker
import time
from util import *

def toml_file():
    with open("apikeys.toml", "r") as f:
        return f.read()

def apikeys_config():
    toml_string = toml_file()
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def setClientsFromFile(abroker):
    apikeys = apikeys_config()["apikeys"]     
    #print ("config " + str(apikeys))
        
    #self.action_logger = setup_actionlogger('action_logger', './log/broker_actions.log')
    #self.action_logger.info("action")
    #self.info_logger = setup_logger('info_logger', './log/broker_info.log')
    
    ck = apikeys["CRYPTOPIA"]    
    
    abroker.set_api_keys(broker.EXC_CRYPTOPIA,ck["public_key"],ck["secret"])
    abroker.set_singleton_exchange(broker.EXC_CRYPTOPIA)
    