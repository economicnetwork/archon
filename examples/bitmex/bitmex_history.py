import datetime
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as bitmex
import archon.exchange.exchanges as exc

brk = Brokerservice()
user_email = "ben@enet.io"
brk.activate_session(user_email)
brk.set_client(exc.BITMEX)
brk.set_client(exc.DELTA)

client = brk.get_client(exc.BITMEX) 
#candles = client.trades_candle("XBTUSD", bitmex.candle_1d)
t1 = datetime.datetime.now()

numdays = 30
candles = client.history_days(numdays)
t2 = datetime.datetime.now()
tt = t2-t1
print ("%i candles fetched in %s"%(len(candles), str(tt)))
