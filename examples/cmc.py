#export COINMARKETCAP_APIKEY='a3a0e86f-9c96-4883-86db-4789d693ce19'
# 
import archon.feeds.cryptocompare as cc
import archon.feeds.coinmarketcap as cmc
import json


def write_data():
    #pdata = cc.get_market_summary()
    #print (pdata)
    #print (len(pdata))

    with open('portal_data.json','w') as f:
        f.write(json.dumps(pdata))


    cmcdata = cmc.get_summary()

    with open('cmc_data.json','w') as f:
        f.write(json.dumps(cmcdata))

"""
coins = cmc.get_description_all() #.values()
for coin in coins:
    print (coin)
    #print (coin["description"])
    #print (coin["name"],coin["symbol"],coin["date_added"])
"""

def write_map_active():
    x = cmc.get_coin_map('active')
    with open('coins_active.csv','w') as f:
        arr = ["id","symbol","name","first_historical_data"]
        s = "|".join([str(x) for x in arr])
        f.write(s + "\n")                
        i = 0
        for z in x:
            print (z)
            arr = [z["id"],z["symbol"],z["name"],z["first_historical_data"]]
            s = "|".join([str(x) for x in arr])
            i+=1
            f.write(s + "\n")

def write_map_inactive():
    x = cmc.get_coin_map('inactive')
    with open('coins_inactive.csv','w') as f:
        arr = ["id","symbol","name","first_historical_data"]
        s = "|".join([str(x) for x in arr])
        f.write(s + "\n")                
        i = 0
        for z in x:
            print (z)
            arr = [z["id"],z["symbol"],z["name"],z["first_historical_data"]]
            s = "|".join([str(x) for x in arr])
            i+=1
            f.write(s + "\n")                

write_map_active()
write_map_inactive()

"""
x = cmc.get_coin_map('active')
i = 0
for z in x:
    print (z)
    print (i,z["name"],z["first_historical_data"])
    i+=1    
"""    