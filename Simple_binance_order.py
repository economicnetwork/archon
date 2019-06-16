"""
binance tickers
"""
import archon.broker.broker as broker
import archon.exchange.exchanges as exc
from archon.exchange.binance import Client as clt
import time

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(path_file_apikeys="C:/trading/archon/examples/binance/apikeys.toml")
client = a.afacade.get_client(exc.BINANCE) 

client.market_order_buy('BTCETH', 0.4, 0.031) #market, amount, price
