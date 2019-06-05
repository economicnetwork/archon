#export COINMARKETCAP_APIKEY='a3a0e86f-9c96-4883-86db-4789d693ce19'
# 
import archon.feeds.cryptocompare as cc
import archon.feeds.coinmarketcap as cmc
import json
import pickle

def write_data():
    #pdata = cc.get_market_summary()
    #print (pdata)
    #print (len(pdata))

    with open('portal_data.json','w') as f:
        f.write(json.dumps(pdata))


    cmcdata = cmc.get_summary()

    with open('cmc_data.json','w') as f:
        f.write(json.dumps(cmcdata))

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

#write_map_active()
#write_map_inactive()
"""
r = cmc.get_description(0)
print (type(r))
for k,v in r.items():
    print (v["description"])
"""


"""
x = cmc.get_coin_map('active')
with open('active_coins.json', 'w') as f:
    f.write(json.dumps(x))
#print (x)
"""

"""
i = 0
for z in x:
    print (z)
    print (i,z["name"],z["first_historical_data"])
    i+=1    
"""    

def load_coins():
    with open('active_coins.json', 'r') as f:
        x = f.read()
        coins = json.loads(x)
        return coins
        
def show_coins():
    coins = load_coins()
    for x in coins:
        has_platform = x["platform"]!=None
        if not has_platform:
            arr = '|'.join(x["id"],x["name"])
            print (x["id"],x["name"])
            #print (x)


def write_out(f, x):
    for z in x[:]:
        has_platform = z["platform"]!=None
        rank = z["cmc_rank"]
        if has_platform:
            arr = '|'.join([str(rank),z['name'],z["platform"]["name"]])
            f.write(arr + '\n')
            #print (rank,z['name'],z["platform"]["name"])
        else:
            arr = '|'.join([str(rank),z['name'],'NA'])
            f.write(arr + '\n')

def get_all():
    x = list()
    x += cmc.get_summary("1")    
    for z in x:
        print (z)

def meta_list(d):
    u = d["urls"]
    #print (u)
    try:
        w = u["website"][0]
    except:
        w = ""
    #announcement
    l = d["logo"]
    id,name,symbol,des,da = d["id"],d["name"],d["symbol"],d["description"],d["date_added"]
    arr = [id,name,symbol,w,des,da]
    return arr


def get_all_meta():    
    #idlist = ','.join([str(x) for x in range(start+1,start+100)])
    #x = cmc.get_description(idlist)        
    print ("get....")
    x = cmc.get_description_all()    
    """
    for k,v in x.items():        
        #print (k,v.keys())
        arr = meta_list(v)
        print (arr)
    """
    #x += cmc.get_summary("201")
    #x += cmc.get_summary("401")
    #x += cmc.get_summary("601")
    #x += cmc.get_summary("801")
    return x

def write_out_meta(f, x):
    for z in x[:]:
        print (z)
        a1 = ""
        a3 = ""
        try:
            a1 = z["urls"]["website"][0]
            a3 = z["urls"]["announcement"][0]
        except:
            pass
            
        a2 = z["logo"]
        a4 = z["name"]
        a5 = z["symbol"]
        a6 = z["description"]
        a7 = str(z["tags"])
        a8 = z["category"]
        a9 = z["date_added"]
        arr = '|'.join([a1,a2,a3,a4,a5,a6,a7,a8])
        f.write(arr + '\n')

coins_meta = get_all_meta()
#for z in coins_meta: 
#    print (z)

fn = 'coins_meta.csv'
with open(fn,'w') as f:
    header = '|'.join(["website",'logo','ann','logo','name','symbol','description','tags','category','date added'])
    f.write(header + '\n')
    write_out_meta(f, coins_meta)

"""
fn = 'coins.csv'
with open(fn,'w') as f:
    arr = '|'.join(["rank",'name','platform'])
    f.write(arr + '\n')
    write_out(f, coins)
"""    

"""
coins = cmc.get_description_all() #.values()
for coin in coins:
    print (coin)
    #print (coin["description"])
    #print (coin["name"],coin["symbol"],coin["date_added"])
"""

