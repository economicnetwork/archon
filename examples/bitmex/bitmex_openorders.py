import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex

abroker = broker.Broker()
abroker.set_active_exchanges([exc.BITMEX])

client = abroker.afacade.get_client(exc.BITMEX)
oo = client.open_orders(mex.instrument_btc_perp)
print (oo)

"""
#BUG
while True:
    oo = abroker.afacade.open_orders(exc.BITMEX)
    print (oo)
    for o in oo:
        print (o['ordStatus'])
    time.sleep(10)
"""