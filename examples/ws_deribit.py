from archon.deribit.ws.Wrapper import DeribitWrapper
import archon.config as config

from archon.ws.broker import WSBroker

wsbroker = WSBroker()

apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

"""
instr = w.getinstruments()

#print (ws.market_depth())

for x in instr:
    k = x['kind']
    if k != 'option':
        print (x)
"""

z = w.getorderbook('BTC-PERPETUAL')
print (z)