"""
find options of deribit
"""

from archon.ws.deribit.Wrapper import DeribitWrapper
import archon.config as config

from archon.ws.broker import WSBroker
from datetime import datetime

wsbroker = WSBroker()

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

def get_options():
    instr = w.getinstruments()
    o = list()
    for x in instr:
        k = x['kind']
        if k == 'option':
            o.append(x)
    return o

def get_options_expiring_soon(opts):
    for x in opts:        
        exp = x['expiration']
        #2019-03-29 08:00:00 GMT
        n = datetime.now()
        dt = datetime.strptime(exp, "%Y-%m-%d %H:%M:%S GMT")
        expiry_from = dt-n
        if expiry_from.days < 20:
            print (x)
                
if __name__=='__main__':                
    options = get_options()                
    print (options)
    get_options_expiring_soon(options)