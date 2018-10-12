"""
standard is 
nominator-denominator e.g. LTC_BTC
"""

import sys, os
import archon.exchange.exchanges as exc

import archon.broker
    
def is_btc(m):
    nom,denom = m.split('_')
    return denom=='BTC'
       
def denom(m):
    nom,denom = m.split('_')
    return denom

def nom(m):
    nom,denom = m.split('_')
    return nom

