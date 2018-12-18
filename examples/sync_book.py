
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.facade as facade
import archon.arch as arch
import archon.markets as m

afacade = facade.Facade()
arch.setClientsFromFile(afacade)
a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX]
a.set_active_exchanges(ae)
market = models.market_from("LTC","BTC")
print ("sync ",market)
a.sync_orderbook_all(market)

db = a.get_db()
x = db.orderbooks.find({'market':market})
for z in x:
    print (z)