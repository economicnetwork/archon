"""
arctic example
"""

import argparse
import json
import csv
import sys
import time

import archon.exchange.exchanges as exc
import archon.exchange.bitmex.bitmex as mex
import datetime
from archon.brokerservice.brokerservice import Brokerservice
from util import *

from arctic import Arctic
import quandl


broker = Brokerservice()

def setup_broker():
    user_id = parse_toml("conf.toml")["user_id"]
    broker.set_apikeys_fromfile(user_id)
    broker.activate_session(user_id)
    broker.set_client(exc.BITMEX)  
    return broker

def write_candles():  
    client = broker.get_client(exc.BITMEX)
    candles = client.trades_candle("XBTUSD", mex.candle_1d)
    candles.reverse()

    # Connect to Local MONGODB
    store = Arctic('localhost')

    # Create the library - defaults to VersionStore
    store.initialize_library('crypto')

    # Access the library
    library = store['crypto']

    library.write('XBTUSD', candles, metadata={'source': 'Bitmex'})


def read_candles():  
    # Connect to Local MONGODB
    store = Arctic('localhost')

    # Create the library - defaults to VersionStore
    store.initialize_library('crypto')

    # Access the library
    library = store['crypto']
    # Reading the data
    item = library.read('XBTUSD')
    xbtusd = item.data

    for x in xbtusd:
        print(x)          

if __name__=='__main__':   
    setup_broker() 
    write_candles()
    read_candles()

