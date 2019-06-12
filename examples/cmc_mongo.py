#export COINMARKETCAP_APIKEY='a3a0e86f-9c96-4883-86db-4789d693ce19'
# 
import archon.feeds.cryptocompare as cc
import archon.feeds.coinmarketcap as cmc
import json
import pickle
from datetime import datetime
from pymongo import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)

def summary():
    cmcdata = cmc.get_summary()

def write_map_active():
    x = cmc.get_coin_map('active')


def write_map_inactive():
    x = cmc.get_coin_map('inactive')
    
def pull_listings():
    db = client['coinmarketcap']
    col = db.coins

    r = cmc.get_listings_all()
    #print (r)
    now = datetime.now() # current date and time
    s = now.strftime("%Y%m%d_%H%M%S")
    
    allkeys = ['id', 'name', 'symbol', 'slug', 'circulating_supply', 'total_supply', 'max_supply', 'date_added', 'num_market_pairs', 'tags', 'platform', 'cmc_rank', 'last_updated', 'quote']
    for x in r:
        cid = col.insert_one(x).inserted_id
        print ("inserted ", cid)

def pull_active():
    x = cmc.get_coin_map('active')
    for z in x:
        print (z)

def show_active():
    db = client['coinmarketcap']
    col = db.coins
    total_mcap = 0
    for x in col.find():
        mcap = x["quote"]["USD"]["market_cap"]
        if mcap != None: total_mcap += mcap
        print (x["id"],x["name"],mcap)

    total_mcap = int(total_mcap)
    i = len(list(col.find()))
    print ("num coins ", i)
    print ("total mcap  ", total_mcap)

def drop_all():
    db = client['coinmarketcap']
    col = db.coins
    col.drop()

if __name__=='__main__':
    pull_active()
    #pull_listings()
    #drop_all()
    #show_active()
    #get_basic()
    
    
