
import archon.exchange.okex as okex
import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
from archon.broker.config import get_keys

keys = get_keys(exc.OKEX)
public_client = okex.OkexClient(key=keys["public_key"],secret=keys["secret"])
ticker = public_client.ticker("ltc_btc")
print (ticker)

#client = okex.OkexTradeClient(key=k,secret=s)
#print (client.balances())
