
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.facade as facade
import archon.broker as broker
import archon.markets as m

afacade = facade.Facade()
broker.setClientsFromFile(afacade)
a = broker.Broker()
ae = [exc.KUCOIN,exc.BITTREX]
a.set_active_exchanges(ae)
market = models.market_from("LTC","BTC")
print ("sync ",market)
a.sync_orderbook_all(market)

db = a.get_db()
x = db.orderbooks.find({'market':market})
for z in x:
    print (z)