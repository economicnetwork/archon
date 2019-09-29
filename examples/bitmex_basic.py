from datetime import datetime

import archon.broker.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.model.models as models
from archon.brokerservice.brokerservice import Brokerservice
#from archon.brokerservice.feeder import Feeder
from archon.util.custom_logger import setup_logger, remove_loggers
from archon.util import *   

if __name__=='__main__':    
    print ("...")
    try:
        #setup service
        #this will init feeder to redis
        abroker = Brokerservice() #setAuto=True)
        abroker.set_apikeys_fromfile(user_id="ben")
        #"apikeys.toml", user_id="ben")
        abroker.activate_session(user_id="ben") #exc.BITMEX, 
        
        #abroker.set_keys_exchange_file(exchanges=[exc.BITMEX]) 
        #time.sleep(1)
        #r = abroker.get_redis()
        #print (r)
        abroker.set_client(exc.BITMEX)
        client = abroker.get_client(exc.BITMEX)
        print ("client ", client)
        
        sym = mex.instrument_btc_perp
        oo = client.open_orders(sym)
        print ("oo ",oo)
        
            
    except Exception as e:
        print ("error ",e)