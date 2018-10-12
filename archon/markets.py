"""
standard is 
nominator-denominator e.g. LTC_BTC
"""

import sys, os
import archon.exchange.exchanges as exc
cwd = os.getcwd()
print (cwd)
#sys.path.append('archon')

import archon.broker
    
def is_btc(m):
    nom,denom = m.split('_')
    return denom=='BTC'

def get_market(nom,denom,exchange):
    if exchange==exc.BITTREX:        
        return denom + '-' + nom
    elif exchange==exc.CRYPTOPIA: 
        return nom + '_' + denom 
    elif exchange==exc.KUCOIN: 
        return nom + '-' + denom  
    elif exchange==exc.HITBTC: 
        return nom + denom  
       
def denom(m):
    nom,denom = m.split('_')
    return denom

def nom(m):
    nom,denom = m.split('_')
    return nom


"""
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