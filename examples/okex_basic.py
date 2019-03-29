
import archon.exchange.okex as okex
import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
from archon.broker.config import parse_toml

from pathlib import Path

def get_keys():
    home = str(Path.home())
    api_file = home + "/.archon/apikeys.toml"
    parsed = parse_toml(api_file)
    return parsed["OKEX"]    

keys = get_keys()
public_client = okex.OkexClient(key=keys["public_key"],secret=keys["secret"])
ticker = public_client.ticker("ltc_btc")
print (ticker)

#client = okex.OkexTradeClient(key=k,secret=s)
#print (client.balances())
