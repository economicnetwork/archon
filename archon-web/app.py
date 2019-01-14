from flask import Flask, render_template
app = Flask(__name__)

from flask import render_template, request, redirect, url_for, redirect
from flask import jsonify
from bson import json_util
import numpy
from pymongo import MongoClient

import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.broker as broker
import archon.model.models as models
import archon.exchange.bitmex.bitmex as mex

abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file()

client = abroker.afacade.get_client(exc.BITMEX)

import logging
import os

@app.route('/data')
def data():
  client = abroker.afacade.get_client(exc.BITMEX)
  candles = client.trades_candle("XBTUSD", mex.candle_1d)
  candles.reverse()
  return jsonify(candles)

@app.route('/')
def home():
  return render_template('index.html')

if __name__ == '__main__':  
  app.run(debug=True,port=8000)
  
  

