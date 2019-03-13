"""
facade raw
no conversion through models
"""

import time
import sys
import time
import random
import json
import logging

import archon.exchange.exchanges as exc
from archon.util import *

#Wrappers
import archon.exchange.rex as bittrex
from archon.exchange.bitmex import bitmex
from archon.exchange.deribit.Wrapper import DeribitWrapper
from archon.util.custom_logger import setup_logger
from archon.exchange.delta.delta_rest_client import DeltaRestClient, create_order_format, cancel_order_format, round_by_tick_size
from archon.model.orders import *


#ORDERSTATUS_COL = 5
ORDERSTATUS = "ORDERSTATUS"
ORDERSTATUS_SUBMITTED = 0
ORDERSTATUS_FILLED = 1
ORDERSTATUS_CANCELLED = 2
ORDERSTATUS_REJECTED = 3

TIMEFRAME_DAILY = "1d"
TIMEFRAME_1HOUR = "1h"
TIMEFRAME_15MINUTE = "15min"
TIMEFRAME_1MINUTE = "1min"


class FacadeRaw:

    def __init__(self):
        setup_logger(logger_name=__name__, log_file='broker.log')
        self.logger = logging.getLogger(__name__)

        self.clients = {}

    def set_api_keys(self, exchange, key, secret):
        """ set clients, assumes conf file present """
        self.logger.info("set api " + str(exchange))
        if exchange==exc.BITMEX:
            self.clients[exchange] = bitmex.BitMEX(apiKey=key, apiSecret=secret)
        elif exchange==exc.DERIBIT:
            self.clients[exchange] = DeribitWrapper(key=key,secret=secret)

    def get_client(self, EXC):
        """ directly get a client """
        return self.clients[EXC]

    def position(self, exchange):
        print (self.clients)
        client = self.clients[exchange]

        if exchange==exc.BITMEX:
            pos = client.position()
            return pos

        elif exchange==exc.DERIBIT:
            pos = client.positions()
            return pos

    def openorders(self, exchange, symbol):
        client = self.clients[exchange]
        if exchange==exc.BITMEX:
            #TODO
            try:                
                oo = client.open_orders(symbol=symbol)
                self.logger.debug("open orders %s"%str(oo))
            except Exception as e:
                self.logger.error("bitmex error %s"%str(e))

        elif exchange==exc.DERIBIT:
                oo = client.getopenorders(symbol)

        return oo

    def orderbook(self, market, exchange=None):
        client = self.clients[exchange]
        self.logger.debug("get orderbook %s %s" %(str(market),exchange))
        #market = models.conv_markets_to(market, exchange)

        if exchange==exc.BITMEX:
            bookdepth = 20
            book = client.market_depth(market,depth=bookdepth)
            #self.logger.debug("book %s"%ob)
            #book = models.conv_orderbook(ob, exchange)
            return book

        elif exchange==exc.DERIBIT:            
            book = client.getorderbook(market)
            #book = models.conv_orderbook(ob, exchange)
            return book            

    def cancel_id(self, oid, otype=None, market=None, exchange=None):
        """ cancel by id """
            
        self.logger.info("cancel " + str(oid) + " " + str(exchange) + " " + str(otype))
        result = None
        client = self.clients[exchange]
        if exchange==exc.BITMEX:
            result = client.cancel(oid)
        elif exchange==exc.DERIBIT:
            result = client.cancel(oid)
        else:
            self.logger.error("no exchange provided")

        self.logger.debug("cancel result " + str(result))
        return result

    def submit_order(self, order, exchange=None):
        """ submit order """

        self.logger.info("submit order " + str(exchange) + " " + str(order))
        market,ttype,order_price,qty = order 
        client = self.clients[exchange]

        #orderD = {"market":market,"type":ttype,"price":order_price,"quantity":qty,"status": ORDERSTATUS_SUBMITTED}

        order_success = False
        order_result = "unkown"
        #order[ORDERSTATUS] = ORDERSTATUS_SUBMITTED
        #self.orders.append(orderD)

        if exchange==exc.BITMEX:
            if ttype==ORDER_SIDE_BUY:
                order_result = client.buy(quantity=qty, price=order_price, symbol=market)
            elif ttype==ORDER_SIDE_SELL:
                order_result = client.sell(quantity=qty, price=order_price, symbol=market)

    def submit_order_post(self, order, exchange=None):
        """ submit order """

        self.logger.info("submit order " + str(exchange) + " " + str(order))
        market,ttype,order_price,qty = order 
        client = self.clients[exchange]

        #orderD = {"market":market,"type":ttype,"price":order_price,"quantity":qty,"status": ORDERSTATUS_SUBMITTED}

        order_success = False
        order_result = "unkown"
        #order[ORDERSTATUS] = ORDERSTATUS_SUBMITTED
        #self.orders.append(orderD)

        if exchange==exc.BITMEX:
            if ttype==ORDER_SIDE_BUY:
                order_result = client.buy_post(quantity=qty, price=order_price, symbol=market)
            elif ttype==ORDER_SIDE_SELL:
                order_result = client.sell_post(quantity=qty, price=order_price, symbol=market)                        
                
        return order_result


