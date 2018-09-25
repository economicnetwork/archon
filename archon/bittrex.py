#!/usr/bin/env python
#import urllib
#import urllib2
from urllib.parse import urlencode
import urllib.request
import json
import time
import hmac
import hashlib
import ssl
import urllib.request



class Client(object):
    
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.baseURL = "https://bittrex.com/api/"
        self.public = ['getmarkets', 'getcurrencies', 'getticker', 'getmarketsummaries', 'getmarketsummary', 'getorderbook', 'getmarkethistory']
        self.market = ['buylimit', 'buymarket', 'selllimit', 'sellmarket', 'cancel', 'getopenorders']
        self.account = ['getbalances', 'getbalance', 'getdepositaddress', 'withdraw', 'getorder', 'getorderhistory', 'getwithdrawalhistory', 'getdeposithistory']
    
    
    def query(self, method, values={}):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        if method in self.public:
            url = self.baseURL + 'v1.1/public/'
        elif method in self.market:
            url = self.baseURL + 'v1.1/market/'            
        elif method in self.account: 
            url = self.baseURL + 'v1.1/account/'
        else:
            return 'Something went wrong, sorry.'
        
        print (values)
        url += method + '?' + urlencode(values)
        print (self.key + " " + self.secret)

        
        
        if method not in self.public:
            url += '&apikey=' + self.key
            url += '&nonce=' + str(int(time.time()))
            signature = hmac.new(self.secret, url, hashlib.sha512).hexdigest()
            headers = {'apisign': signature}
        else:
            headers = {}

        print ("query " + url)            
        
        req = urllib.request.Request(url, headers=headers)
        response = json.loads(urllib.request.urlopen(req, context = ctx).read())
        
        if response["result"]:
            return response["result"]
        else:
            return response["message"]

    def getmarkets(self):
        return self.query('getmarkets')
    
    def getcurrencies(self):
        return self.query('getcurrencies')
    
    def getticker(self, market):
        return self.query('getticker', {'market': market})
    
    def getmarketsummaries(self):
        return self.query('getmarketsummaries')
    
    def getmarketsummary(self, market):
        return self.query('getmarketsummary', {'market': market})
    
    def getorderbook(self, market, type, depth=20):
        return self.query('getorderbook', {'market': market, 'type': type, 'depth': depth})
    
    def getmarkethistory(self, market, count=20):
        return self.query('getmarkethistory', {'market': market, 'count': count})
    
    def buylimit(self, market, quantity, rate):
        return self.query('buylimit', {'market': market, 'quantity': quantity, 'rate': rate})
    
    def buymarket(self, market, quantity):
        return self.query('buymarket', {'market': market, 'quantity': quantity})
    
    def selllimit(self, market, quantity, rate):
        return self.query('selllimit', {'market': market, 'quantity': quantity, 'rate': rate})
    
    def sellmarket(self, market, quantity):
        return self.query('sellmarket', {'market': market, 'quantity': quantity})
    
    def cancel(self, uuid):
        return self.query('cancel', {'uuid': uuid})
    
    def getopenorders(self, market):
        return self.query('getopenorders', {'market': market})
    
    def getbalances(self):
        return self.query('getbalances')
    
    def getbalance(self, currency):
        return self.query('getbalance', {'currency': currency})
    
    def getdepositaddress(self, currency):
        return self.query('getdepositaddress', {'currency': currency})
    
    def withdraw(self, currency, quantity, address):
        return self.query('withdraw', {'currency': currency, 'quantity': quantity, 'address': address})
    
    def getorder(self, uuid):
        return self.query('getorder', {'uuid': uuid})
    
    def getorderhistory(self, market, count):
        return self.query('getorderhistory', {'market': market, 'count': count})
    
    def getwithdrawalhistory(self, currency, count):
        return self.query('getwithdrawalhistory', {'currency': currency, 'count': count})
    
    def getdeposithistory(self, currency, count):
        return self.query('getdeposithistory', {'currency': currency, 'count': count})            