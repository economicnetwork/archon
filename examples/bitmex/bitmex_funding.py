from datetime import datetime

import archon.broker.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.model.models as models
from archon.brokerservice.brokerservice import Brokerservice
#from archon.brokerservice.feeder import Feeder
from archon.util.custom_logger import setup_logger, remove_loggers
from archon.util import *   

from arctic import Arctic

# Connect to Local MONGODB
store = Arctic('localhost')

# Create the library - defaults to VersionStore
store.initialize_library('Crypto')


def store_series(client):
    sym = mex.instrument_btc_perp

    candles = client.trades_candle("XBTUSD", mex.candle_1d)
    print (candles)
    print (len(candles))

    """
        with open('bitmex_candles.csv','w') as f:
            for x in candles:
                f.write(str(x) + '\n')
    """

def store_funding(client):   

        sym = mex.instrument_btc_perp
        oo = client.open_orders(sym)
        print ("oo ",oo)

        s1 = '2018-09-01T00:00:00.000Z'
        f1 = client.funding(s1)
        s2 = '2019-02-14T12:00:00.000Z'
        f2 = client.funding(s2)
        s3 = '2019-07-30T20:00:00.000Z'
        f3 = client.funding(s3)

        allfunding = f1 + f2 + f3
        print (len(allfunding))
        print (allfunding[-1])

        """
        with open('bitmex_funding.csv','w') as f:
            for x in all:
                f.write(str(x) + '\n')

        """
        library = store['Crypto']
        library.write('XBTUSD_funding', allfunding, metadata={'source': 'Bitmex'})

if __name__=='__main__':    
    print ("...")
    try:
        abroker = Brokerservice() #setAuto=True)
        abroker.set_apikeys_fromfile(user_id="ben")
        abroker.activate_session(user_id="ben") #exc.BITMEX, 
        
        abroker.set_client(exc.BITMEX)
        client = abroker.get_client(exc.BITMEX)
        print ("client ", client)
        
        #store_series(client)

        library = store['Crypto']

        #library.write('XBTUSD', candles, metadata={'source': 'Bitmex'})

        #item = library.read('XBTUSD')
        #xbtusd = item.data
        #print (xbtusd)

        store_funding(client)

        

        
            
    except Exception as e:
        print ("error ",e)