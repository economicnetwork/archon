import requests
import json
import os
import time

import archon.exchange.exchanges as exc
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.exchanges as exc

brk = Brokerservice()
user_email = "my@email.io" #os.environ["USER_EMAIL"]
brk.store_apikey(exc.BINANCE, "", "", user_id=user_email)