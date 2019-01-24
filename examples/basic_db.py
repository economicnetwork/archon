import archon.exchange.exchanges as exc
import archon.broker as broker
import pymongo

import archon.broker as broker
import archon.exchange.exchanges as exc

abroker = broker.Broker(setAuto=False)
#abroker.set_active_exchanges([exc.BINANCE])

db = abroker.get_db()

#l = db.
#.find_one({"exchange":"Kucoin"})
#for x in l['candles']:
#    print (x)
