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
#btc = client.market_order_buy() # commented out lines are just to play around with
#t = client.get_all_tickers()
#print (client.get_account()) ## added 

client.get_ticker() = ('BTCETH', 0.4, 0.031) #market, amount, price

#for x in t[:10]:
#   print (x)
#    a = broker.Broker(setAuto=False)