"""
redis simple test
"""
import redis
from archon.config import *

confFile = "conf.toml"
try:
    all_conf = parse_toml(confFile)
except:
    print("config file %s not properly formatted"%str(confFile))

redis_conf = all_conf["REDIS"]       
host = redis_conf["host"]     
port = redis_conf["port"]
redis_client = redis.Redis(host=host, port=port)
redis_client.set("test","test")
x = redis_client.get("test")
print (x)