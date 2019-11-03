from numpy import array
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import datetime
from archon.brokerservice.brokerservice import Brokerservice
from util import *

from archon.util import *

import pandas as pd
import numpy
import matplotlib.pyplot as plt
from arctic import Arctic

import argparse
import json
import csv
import sys
import time


from arctic import Arctic
import quandl

broker = Brokerservice()

def setup_broker():
    user_id = parse_toml("conf.toml")["user_id"]
    broker.set_apikeys_fromfile(user_id)
    broker.activate_session(user_id)
    broker.set_client(exc.BITMEX)  
    return broker

candles = client.trades_candle("XBTUSD", mex.candle_1d)
candles.reverse()
closes = list()
COL_CLOSE = 'close'
COL_VOLUME = 'volume'

closes = [float(z[COL_CLOSE]) for z in candles]
volumes = [float(z[COL_VOLUME]) for z in candles]
dates = [z['timestamp'] for z in candles]

raw_data = {'close': closes, 'volume': volumes}

df = pd.DataFrame(raw_data, index=dates, columns = ['close', 'volume'])