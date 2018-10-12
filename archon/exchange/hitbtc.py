"""
Hitbtc wrapper
API docs
https://github.com/hitbtc-com/hitbtc-api/blob/master/APIv2.md
"""

import uuid
import time

import requests
from decimal import *

API_BASE = "https://api.hitbtc.com"

class RestClient(object):

    def __init__(self, public_key, secret):                
        self.init(public_key, secret)

    #def __init__(self, config):                
    #    self.init(config["public_key"], config["secret"])

    def init(self, public_key, secret):        
        self.url = API_BASE + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    # ------ PUBLIC --------

    def get_request(self, endpoint,params=None):
        """ request with retries """
        done = False
        tries = 0
        while not done:
            try:
                if params:                
                    result = self.session.get("%s/%s" % (self.url,endpoint), params=params)
                else:
                    result = self.session.get("%s/%s" % (self.url, endpoint))
                #print (result)
                jresult = result.json()
                return jresult
            except ConnectionError:                
                tries +=1
                if tries > 10:
                    raise ConnectionError
                else:
                    pass

    def get_currenices(self):
        #GET /api/2/public/currency
        return self.get_request("public/currency")

    def get_tickers(self):
        return self.get_request("public/ticker")

    def get_ticker(self, symbol):
        return self.get_request("public/ticker/%s" % (symbol))

    def get_symbols(self):
        """Get symbol."""
        return self.get_request("public/symbol")

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.get_request("public/symbol/%s" % (symbol_code))

    def get_candles(self, symbol_code):
        """
        limit   Number  Limit of candles, default 100.
        period  String  One of: M1 (one minute), M3, M5, M15, M30, H1, H4, D1, D7, 1M (one month). Default is M30 (30 minutes).
        #GET /api/2/public/candles/{symbol}
        """

        #return self.session.get("%s/public/candles/%s" % (self.url, symbol_code)).json()   
        data = {'limit': 100, 'period': 'D1'}
        ret = self.session.get("%s/public/candles/%s" % (self.url, symbol_code), params=data)
        #ret = self.session.get("%s/public/candles/%s" % (self.url, symbol_code))        
        return ret.json()
        #return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()
        #return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        try:
            ob = self.get_request("public/orderbook/%s" % (symbol_code))
            return ob
        except ConnectionError:
            print ("failed getting orderbook")


    def get_market_trades(self, symbol_code):
        return self.get_request("public/trades/%s" % (symbol_code))
        
    # ------ PRIVATE --------

    def get_orders(self):
        return self.get_request("order")

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.get_request("account/crypto/address/%s" % (currency_code))

    def get_account_balance(self):
        """Get main balance."""
        return self.get_request("account/balance")

    def get_trading_balance(self):
        """Get trading balance."""
        return self.get_request("trading/balance")

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()

    def submit_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        print("submit order ", symbol_code," ",side," ",price," ",quantity)
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}

        if price is None:
            raise Exception("needs limit price")
        else:
            data['price'] = price            
        try: 
            result = self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()
            return result
        except:
            print("Unexpected error submit order:", sys.exc_info()[0])
            raise


    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def get_trades(self):
        data = {'limit': 1000}
        result = self.get_request("history/trades", params=data)
        return result

    def cancel_order(self, client_order_id):
        """Cancel order."""
        print ("cancel", client_order_id)
        r = self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()
        print (r)
        return r

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_trades_symbol(self, symbol):
        """Get transaction info."""
        """
        data = {'symbol': symbol}
        ret = self.session.get("%s/history/trades" % self.url, data=data)
        print (ret)
        return ret.json()
        """
        trades = self.get_trades()
        st = list()
        for t in trades:
            if t["symbol"] == symbol:
                st.append(t)
        return st

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.get_request("account/transactions/%s" % (transaction_id))

    def get_transactions(self):
        """Get all transaction info."""
        return self.get_request("account/transactions")
