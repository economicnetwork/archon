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

def get_options():
    instr = w.getinstruments()
    o = list()
    for x in instr:
        k = x['kind']
        if k == 'option':
            o.append(x)
    return o

def get_options_expiring_soon(opts):
    print ("** options expring in next 20 days ** ")
    for x in opts:        
        exp = x['expiration']
        #2019-03-29 08:00:00 GMT
        n = datetime.now()
        dt = datetime.strptime(exp, "%Y-%m-%d %H:%M:%S GMT")
        expiry_from = dt-n
        if expiry_from.days < 40:
            #{'kind': 'option', 'baseCurrency': 'BTC', 'currency': 'USD', 'minTradeSize': 0.1, 
            # 'instrumentName': 'BTC-4JAN19-4000-C', 'isActive': True, 
            # 'settlement': 'week', 'created': '2018-12-27 08:00:02 GMT', 
            # 'tickSize': 0.0005, 'pricePrecision': 4, 'expiration': '2019-01-04 08:00:00 GMT',
            #  'strike': 4000.0, 'optionType': 'call'}
            try:
                s = x['strike']
                ot = x['optionType']
                inst = x['instrumentName']
                summary = w.getsummary(inst)
                ask = float(summary['askPrice'])
                bid = float(summary['bidPrice'])
                spread = (ask-bid)/ask
                print (s,ot,exp,summary['last'],spread)
            except:
                continue
            
                
if __name__=='__main__':                
    options = get_options()                
    #print (options)
    get_options_expiring_soon(options)