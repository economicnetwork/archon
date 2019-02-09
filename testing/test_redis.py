"""
redis simple test
"""
import redis
from archon.config import *

redis_client = redis.Redis(host="localhost", port=6379)
redis_client.set("test","test")
x = redis_client.get("test")
print (x)