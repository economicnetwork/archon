from archon.exchange.bitmex import bitmex
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(keys_filename="bitmex.toml")
client = a.afacade.get_client(exc.BITMEX)

path = "trade"
count = 100
query = {
    'reverse': 'false',
    'start': 0,
    'count': count,
    #'filter': args.filter
}

data = client._curl_bitmex(path=path, verb="GET", query=query, timeout=10)
print (data)
