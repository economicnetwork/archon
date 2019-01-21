"""
find options of deribit
"""

from archon.exchange.deribit.Wrapper import DeribitWrapper
import archon.config as config

from datetime import datetime

abroker = broker.Broker(setAuto=False)
abroker.set_keys_exchange_file(exchanges=[exc.DERIBIT])


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
"""    