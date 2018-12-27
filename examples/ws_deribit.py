from archon.ws.deribit.Wrapper import DeribitWrapper
import archon.arch as a

apikeys = a.parse_toml("apikeys.toml")

k = apikeys["DERIBIT"]["public_key"]
s = apikeys["DERIBIT"]["secret"]
w = DeribitWrapper(key=k,secret=s)

print (w.getinstruments())