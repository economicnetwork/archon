"""
simple test
"""
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client["broker-db"]
db.testing.insert_one({"test":"test"})
x = list(db.testing.find({}))
print (x)
db.testing.drop()