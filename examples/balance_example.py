
import archon.exchange.exchanges as exc
import archon.broker as broker
import archon.arch as arch

a = arch.Arch()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

bl = list()
for e in ae:
    b = a.abroker.balance_all(exchange=e)
    for x in b:
        n = exc.NAMES[e]
        x['exchange'] = n
        s = x['symbol']
        print (x)
        
