import requests
import json
import os
import time

from archon.exchange.delta.delta_rest_client import create_order_format, cancel_order_format, round_by_tick_size
from archon.exchange.delta.instruments import btc_march, btc_march_quanto, btc_june, product_names
import archon.exchange.exchanges as exc
from archon.plugins.aws_ses import AwsSes
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.exchanges as exc

brk = Brokerservice()
user_email = "my@email.io" #os.environ["USER_EMAIL"]
brk.activate_session(user_email)
brk.set_client(exc.BINANCE)
binance_client = brk.get_client(exc.BINANCE)    

market = "BATBTC"
orderbook = binance_client.get_orderbook_symbol(market)    
print (orderbook)