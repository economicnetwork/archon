
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch

abroker = broker.Broker()
arch.setClientsFromFile(abroker)

bl = list()
for e in [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.BINANCE]:
    b = abroker.balance_all(exchange=e)
    for x in b:
        n = exc.NAMES[e]
        x['exchange'] = n
        s = x['symbol']
        t = float(x['total'])
        if t > 0:
            print (x)

