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

x = client.getlasttrades(sym)
for y in x:
    print (y)