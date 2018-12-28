from archon.ws.deribit.Wrapper import DeribitWrapper
import archon.config as config

from archon.ws.broker import WSBroker

wsbroker = WSBroker()

"""
apikeys = config.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

print (w.getinstruments())
"""