from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime,timezone,timedelta

abroker = broker.Broker(setAuto=True)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT]) 
client = abroker.afacade.get_client(exc.DERIBIT)



def convert_time(ts):
    return datetime.utcfromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S')

def get_trades(sym, dt):        
    ts = 1000*int(dt.timestamp())
    #print(ts)

    start = ts
    z = client.getlasttrades(sym,start=start,end=start+10**8,count=1)
    return z

def show(sym):    
    dt = datetime(2018, 12, 1)
    dt = dt.replace(tzinfo=timezone.utc)
    z = get_trades(sym, dt)

    for x in z:
        tsf = convert_time(x['timeStamp'])
        print (tsf,x['price'])

def show2():
    z = client.getlasttrades_seq(sym,startSeq=1,endSeq=1000,count=1)
    for x in z:
        ts = x['timeStamp']
        tsf = convert_time(ts)
        print (tsf,x['price'])


#show2()   
#sym = 'BTC-PERPETUAL'     
sym = deribit.instrument_btc_march
show(sym)