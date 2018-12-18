
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker

a = broker.Broker()
ae = [exc.KUCOIN,exc.BITTREX,exc.CRYPTOPIA,exc.HITBTC,exc.BINANCE]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()


def individual_balance():
    bl = list()
    for e in ae:
        b = a.afacade.balance_all(exchange=e)
        for x in b:
            n = exc.NAMES[e]
            x['exchange'] = n
            s = x['symbol']
            print (x)
            
def balance_currency():
    bl = a.global_balances()
    btc = list(filter(lambda d: d['symbol']=='BTC', bl))
    print (btc)

balance_currency()