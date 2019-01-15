"""
find options of deribit
"""

from archon.ws.deribit.Wrapper import DeribitWrapper
import archon.config as config

from datetime import datetime

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

def instr():
    instr = w.getinstruments()
    o = list()
    for x in instr:
        k = x['kind']
        if k != 'option':
            print (x)
    
                
if __name__=='__main__':                
    instr()

"""
BTC-PERPETUAL
BTC-28JUN19
BTC-29MAR19
"""    