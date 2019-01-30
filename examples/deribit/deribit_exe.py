from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime
from archon.custom_logger import setup_logger, remove_loggers, remove_all_loggers

abroker = broker.Broker(setAuto=True, setMongo=False)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT]) 
client = abroker.afacade.get_client(exc.DERIBIT)
remove_all_loggers()
#remove_loggers()
sym = 'BTC-PERPETUAL'

th = client.tradehistory()
for x in th:
    ts = x['timeStamp']
    ts = int(ts)/1000
    tsf = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    q = x['quantity']
    p = x['price']
    s = x['side']

    print(tsf,q,p,s)
    