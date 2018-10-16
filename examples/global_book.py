
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.broker as broker
import archon.arch as arch
import archon.markets as m

abroker = broker.Broker()
arch.setClientsFromFile(abroker)
a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA]
a.set_active_exchanges(ae)
market = models.market_from("LTC","BTC")
print ("sync ",market)
a.sync_orderbook_all(market)
[allbids,allasks] = a.global_orderbook(market)

for b in allbids[:5]:
    print (b)

for a in allasks[:5]:
    print (a)    