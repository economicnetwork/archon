"""
standard is 
nominator-denominator e.g. LTC_BTC
"""

import sys, os
import archon.exchange.exchanges as exc
cwd = os.getcwd()
print (cwd)
#sys.path.append('archon')

import archon.broker as broker
    
def convert_markets_to(m, exchange):
    if exchange==exc.CRYPTOPIA:
        nom,denom = m.split('/')
        return nom + '_' + denom
    elif exchange==exc.BITTREX:    
        denom,nom = m.split('-')
        return nom + '_' + denom

def convert_markets_from(m, exchange):
    if exchange==exc.CRYPTOPIA:
        nom,denom = m.split('_')
        return nom + '_' + denom
    elif exchange==exc.BITTREX:    
        nom,denom = m.split('_')
        return denom + '-' + nom

def denom(m):
    nom,denom = m.split('_')
    return denom

def nom(m):
    nom,denom = m.split('_')
    return nom


def market_obj(m_str, exchange):
    if exchange==exc.CRYPTOPIA:
        nom,denom = m_str.split('/')
        return Market(nom, denom)
    elif exchange==exc.BITTREX:    
        denom,nom = m_str.split('-')
        return Market(nom, denom)



def market_summary(d, exchange):
    if exchange==exc.CRYPTOPIA:
        #{'TradePairId': 5328, 'Label': 'NLC2/BTC',
        # 'AskPrice': 2.23e-06, 'BidPrice': 2.2e-06, 
        #'Low': 2.19e-06, 'High': 2.52e-06, 
        #'Volume': 453456.10265629, 'LastPrice': 2.22e-06, 'BuyVolume': 5336288.27376562, 'SellVolume': 3148220.6228541, 'Change': -9.02, 'Open': 2.44e-06, 'Close': 2.22e-06, 
        #'BaseVolume': 1.069483, 'BuyBaseVolume': 0.91884075, 'SellBaseVolume': 901.01625399}
        ask = d['AskPrice']
        bid = d['BidPrice']
        last = d['LastPrice']
        volume = d['BaseVolume']
        return {'ask':ask,'bid':bid,'last':last,'volume':volume}
    elif exchange==exc.BITTREX:
        #{'MarketName': 'BTC-NLC2', 'High': 2.67e-06, 'Low': 2.25e-06, 
        #'Volume': 932113.81209525, 'Last': 2.25e-06, 'BaseVolume': 2.25302657, 
        #'TimeStamp': '2018-09-25T08:05:30.613', 'Bid': 2.25e-06,
        # 'Ask': 2.27e-06, 'OpenBuyOrders': 63, 'OpenSellOrders': 436, 
        #'PrevDay': 2.48e-06, 'Created': '2018-06-21T18:54:34.747'}
        ask = d['Ask']
        bid = d['Bid']
        last = d['Last']
        volume = d['BaseVolume']
        return {'ask':ask,'bid':bid,'last':last,'volume':volume}





"""
#from . import broker
#import archon.broker as broker

class Market:

    def __init__(self, from_market, to_market, exchange):
        self.from_market = from_market
        self.to_market = to_market
        self.exchange = exchange
        self.exchange_name = exc.NAMES[exchange]

    def __init__(self, market_string, exchange):
        if exchange==exc.CRYPTOPIA:
            delim = '/'
            nom,denom = market_string.split(delim)
            super(nom, denom, exchange)            
        elif exchange==exc.BITTREX:
            delim = '-'
            denom,nom = market_string.split(delim)
            super(nom, denom, exchange)                    

    def str_rep(self):
        ''' string representation '''
        #nom,denom = m.split('/')
        if self.exchange==exc.CRYPTOPIA:
            delim = '/'
            srep = delim.join([self.from_market, self.to_market])
            return srep
        elif self.exchange==exc.BITTREX:
            delim = '-'
            srep = delim.join([self.to_market, self.from_market])
            return srep            

    def __str__(self):
        return "%s: [%s - %s]"%(self.exchange_name,self.from_market,self.to_market)
"""