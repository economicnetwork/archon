"""
Cryptopia

https://support.cryptopia.co.nz/csm?id=kb_article&sys_id=a75703dcdbb9130084ed147a3a9619bc
https://support.cryptopia.co.nz/csm?id=kb_article&sys_id=40e9c310dbf9130084ed147a3a9619eb
"""

import json
import time
import hmac
import hashlib
import base64
import requests

# using requests.compat to wrap urlparse
from requests.compat import quote_plus

class CryptopiaAPI(object):
    """ Represents a wrapper for cryptopia API """

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.public = ['GetCurrencies', 'GetTradePairs', 'GetMarkets',
                       'GetMarket', 'GetMarketHistory', 'GetMarketOrders', 'GetMarketOrderGroups']
        self.private = ['GetBalance', 'GetDepositAddress', 'GetOpenOrders',
                        'GetTradeHistory', 'GetTransactions', 'SubmitTrade',
                        'CancelTrade', 'SubmitTip', 'SubmitWithdraw', 'SubmitTransfer']

    def api_query(self, feature_requested, get_parameters=None, post_parameters=None):
        """ query host and retry if fails """
        retires = 10
        done = False    
        i = 0
        #print ("query " + feature_requested)
        while not done:            
            result, error = self.api_query_request(feature_requested, get_parameters, post_parameters)
            #print ("got result " + str(result))
            if error:
                print ("error ? " + str(error))
                print (feature_requested)
            #print (result)
            #print (error)
            if not error and result != None:
                return result, error
            else:                
                i+=1
                print ("request failed. retry")
                if i > retires:
                    if result == None:
                        return None, "none returned"
                    else:
                        return result, error


    def api_query_request(self, feature_requested, get_parameters=None, post_parameters=None):
        """ Performs a generic api request """
        time.sleep(1)
        baseURL = "https://www.cryptopia.co.nz/Api/"
        if feature_requested in self.private:
            url = baseURL + feature_requested
            post_data = json.dumps(post_parameters)
            headers = self.secure_headers(url=url, post_data=post_data)
            req = requests.post(url, data=post_data, headers=headers)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            req.encoding = "utf-8-sig"
            req = req.json()
            if 'Success' in req and req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                error = req['Error'] if 'Error' in req else 'Unknown Error'
            return (result, error)
        elif feature_requested in self.public:
            url = baseURL + feature_requested + "/" + \
                  ('/'.join(i for i in get_parameters.values()
                           ) if get_parameters is not None else "")
            #print ("request url " + url)
            req = requests.get(url, params=get_parameters)
            if req.status_code != 200:
                try:
                    req.raise_for_status()
                except requests.exceptions.RequestException as ex:
                    return None, "Status Code : " + str(ex)
            req = req.json()
            if req == None:
                error = "no reply"
                result = None
                return (result, error)
            if 'Success' in req and req['Success'] is True:
                result = req['Data']
                error = None
            else:
                result = None
                error = req['Error'] if 'Error' in req else 'Unknown Error'
            return (result, error)
        else:
            return None, "Unknown feature"

    # ------- public -------
    
    def get_currencies(self):
        """ Gets all the currencies """
        return self.api_query(feature_requested='GetCurrencies')

    def get_tradepairs(self):
        """ Gets all the trade pairs """
        return self.api_query(feature_requested='GetTradePairs')

    def get_markets(self):
        """ Gets data for all markets """
        return self.api_query(feature_requested='GetMarkets')

    def get_market(self, market):
        """ Gets market data """
        return self.api_query(feature_requested='GetMarket',
                              get_parameters={'market': market})

    def get_history(self, market):
        """ Gets the full order history for the market (all users) """
        return self.api_query(feature_requested='GetMarketHistory',
                              get_parameters={'market': market})

    def get_history_candle(self, market):
        return self.api_query(feature_requested='GetMarketHistory',
                              get_parameters={'market': market, 'hours': '24'})
        
    def get_orders(self, market):
        """ orderbook """        
        return self.api_query(feature_requested='GetMarketOrders',
                              get_parameters={'market': market})

    """
    def get_ordergroups(self, markets):
        #Gets the order groups for the specified market
        return self.api_query(feature_requested='GetMarketOrderGroups',
                              get_parameters={'markets': markets})
    """

    # ------- private -------

    def get_balance_all(self):
        """ Gets the balance of the user in the specified currency """        
        result, error = self.api_query(feature_requested='GetBalance',
                                       post_parameters={})
        return (result, error)        


    def get_balance(self, currency):
        """ Gets the balance of the user in the specified currency """        
        result, error = self.api_query(feature_requested='GetBalance',
                                       post_parameters={'Currency': currency})        
        if error is None:
            result = result[0]
        return (result, error)

    def get_openorders(self, market):
        """ Gets the open order for the user in the specified market """
        return self.api_query(feature_requested='GetOpenOrders',
                              post_parameters={'Market': market})

    def get_openorders_all(self):
        """ Gets the open order for the user  """
        return self.api_query(feature_requested='GetOpenOrders',
                              post_parameters={})

    def get_deposit_address(self, currency):
        """ Gets the deposit address for the specified currency """
        return self.api_query(feature_requested='GetDepositAddress',
                              post_parameters={'Currency': currency})

    def get_tradehistory(self, market):
        """ Gets the trade history for a market """
        return self.api_query(feature_requested='GetTradeHistory',
                              post_parameters={'Market': market, 'Count': 10000})

    def get_tradehistory_all(self):
        """ Gets the trade history """
        return self.api_query(feature_requested='GetTradeHistory',
                              post_parameters={'Count': 10000})

    def get_transactions(self, transaction_type):
        """ Gets all transactions (deposits, withdraws) for a user """
        return self.api_query(feature_requested='GetTransactions',
                              post_parameters={'Type': transaction_type})

    # ------- actions -------

    def submit_trade(self, market, trade_type, rate, amount):
        """ Submits a trade """
        return self.api_query(feature_requested='SubmitTrade',
                              post_parameters={'Market': market,
                                               'Type': trade_type,
                                               'Rate': rate,
                                               'Amount': amount})

    def cancel_trade(self, trade_type, order_id, tradepair_id):
        """ Cancels an active trade """
        return self.api_query(feature_requested='CancelTrade',
                              post_parameters={'Type': trade_type,
                                               'OrderID': order_id,
                                               'TradePairID': tradepair_id})

    def cancel_trade_id(self, order_id):
        """ Cancels an active trade """
        r = self.api_query(feature_requested='CancelTrade',
                              post_parameters={'Type': 'Trade',
                                               'OrderID': order_id})
        print ("cancel result " + str(r))
        return r

    def cancel_all_trades(self):
        """ Cancels an active trade """
        return self.api_query(feature_requested='CancelTrade',
                              post_parameters={'Type': 'ALL'})
    
    def submit_tip(self, currency, active_users, amount):
        """ Submits a tip """
        return self.api_query(feature_requested='SubmitTip',
                              post_parameters={'Currency': currency,
                                               'ActiveUsers': active_users,
                                               'Amount': amount})

    def submit_withdraw(self, currency, address, amount):
        """ Submits a withdraw request """
        return self.api_query(feature_requested='SubmitWithdraw',
                              post_parameters={'Currency': currency,
                                               'Address': address,
                                               'Amount': amount})

    def submit_transfer(self, currency, username, amount):
        """ Submits a transfer """
        return self.api_query(feature_requested='SubmitTransfer',
                              post_parameters={'Currency': currency,
                                               'Username': username,
                                               'Amount': amount})

    def secure_headers(self, url, post_data):
        """ Creates secure header for cryptopia private api. """
        nonce = str(time.time() )
        md5 = hashlib.md5()
        jsonparams = post_data.encode('utf-8')
        md5.update(jsonparams)
        rcb64 = base64.b64encode(md5.digest()).decode('utf-8')
        
        signature = self.key + "POST" + quote_plus(url).lower() + nonce + rcb64
        hmacsignature = base64.b64encode(hmac.new(base64.b64decode(self.secret),
                                                  signature.encode('utf-8'),
                                                  hashlib.sha256).digest())
        header_value = "amx " + self.key + ":" + hmacsignature.decode('utf-8') + ":" + nonce
        return {'Authorization': header_value, 'Content-Type': 'application/json; charset=utf-8'}
