from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime

abroker = broker.Broker(setAuto=True)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT]) 
client = abroker.afacade.get_client(exc.DERIBIT)

sym = 'BTC-PERPETUAL'


from datetime import timezone
dt = datetime(2019, 1, 10)
ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
print(ts)

ts = 1548475974312
z = client.getlasttrades(sym,count=100,since=ts)
for x in z:
    ts = x['timeStamp']
    print (ts)
    ts = int(ts)/1000
    tsf = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print (tsf)