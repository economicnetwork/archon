
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.facade as facade
import archon.arch as arch
import archon.markets as m

a = arch.Arch()
#ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
ae = [exc.BINANCE]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

market = models.market_from("LTC","BTC")

[allbids,allasks,ts]  = a.get_global_orderbook(market)

print ("global orderbook %s"%market)
print ("bids")
for b in allbids[:5]:
    print (b)

print ('*********')
print ("asks")
for a in allasks[:5]:
    print (a)   

topbid = float(allbids[0]['price'])
topask = float(allasks[0]['price'])
spread = (topask-topbid)/topbid
print ("spread ",spread)
