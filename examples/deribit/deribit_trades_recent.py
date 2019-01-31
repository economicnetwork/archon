from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime,timezone,timedelta

abroker = broker.Broker(setAuto=True)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT]) 
client = abroker.afacade.get_client(exc.DERIBIT)

t = client.getlasttrades_recent(deribit.instrument_btc_perp)
for x in t:
    print (x)