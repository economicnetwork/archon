"""
broker service
* is used by an external webapp
* user data is stored in the external webapp
* external process will register call back to get user_data
* broker stores all exchange relevant data: balances, orders, ...
"""

import json
import os
import datetime
import time
from pymongo import MongoClient
import logging
import redis

from archon.config import *
import archon.brokersrv.facader as facader
import archon.exchange.exchanges as exc
from archon.model import models
import archon.orderbooks as orderbooks
from archon.feeds import cryptocompare
from archon.util import *
from archon.util.custom_logger import setup_logger, remove_loggers

class BrokerService:

    def __init__():
        pass
        
    def set_mongo(self, uri):        
        self.logger.debug("using mongo %s"%str(uri))
        mongoclient = MongoClient(uri)
        self.db = mongoclient["broker-db"]

        self.get_users_callback = None
        
    def get_redis(self):
        return self.redis_client

    def get_db(self):
        return self.db

    def get_balances(self, user_id):
        #exchange
        self.balances.find({"user_id": user_id})

    def register_user_callback(self, user_id, cb):
        self.user_callbacks[user_id] = cb

    def register_userlist_callback(self, cb):
        self.register_userlist_callback = cb

    def sync_balance(app):
        """ sync all """
        global client
        users = self.get_users_callback()
        for user in users:
            print (user)

            """
            if client is None: 
                client = get_client(user)        
            else:
                pass
                #if lastuser = user:
                    
            funds = [{exc.BITMEX_NAME:client.funds()}]
            app.mongo.db.users.update_one({"email": user["email"]}, {"$set": {"funds": funds}})
            """

            
                       

