from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client["broker-db"]
xmarkets = list(db.markets.find({}))
print (xmarkets)