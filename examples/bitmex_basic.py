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

        candles = client.trades_candle("XBTUSD", mex.candle_1d)
        print (candles)
        print (len(candles))

        with open('bitmex_candles.csv','w') as f:
            for x in candles:
                f.write(str(x) + '\n')

        """
        oo = client.open_orders(sym)
        print ("oo ",oo)

        s1 = '2018-09-01T00:00:00.000Z'
        f1 = client.funding(s1)
        s2 = '2019-02-14T12:00:00.000Z'
        f2 = client.funding(s2)
        s3 = '2019-07-30T20:00:00.000Z'
        f3 = client.funding(s3)

        all = f1 + f2 + f3
        print (len(all))
        print (all[-1])

        with open('bitmex_funding.csv','w') as f:
            for x in all:
                f.write(str(x) + '\n')

        """
        
            
    except Exception as e:
        print ("error ",e)