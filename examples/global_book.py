
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
#a.sync_orderbook_all(market)

[allbids,allasks,ts]  = a.get_global_orderbook(market)

print ("global orderbook %s"%market)
for b in allbids[:15]:
    print (b)

print ('*********')
for a in allasks[:15]:
    print (a)    
