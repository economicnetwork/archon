import datetime
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as bitmex
import archon.exchange.exchanges as exc
import pandas as pd
import numpy
import matplotlib.pyplot as plt
#from arctic import Arctic
from boto3 import client


import boto3
import requests
import json
import matplotlib.pyplot as plt

brk = Brokerservice()
user_email = "ben@enet.io"
brk.activate_session(user_email)
brk.set_client(exc.BITMEX)
brk.set_client(exc.DELTA)

bitmex_client = brk.get_client(exc.BITMEX) 
#candles = client.trades_candle("XBTUSD", bitmex.candle_1d)

numdays = 500

def write_candles(candles):
    with open("history.csv", "w") as f:
        for c in candles:
            f.write(str(c) + "\n")
        

def fetch():
    t1 = datetime.datetime.now()
    
    candles = bitmex_client.history_days(numdays)
    t2 = datetime.datetime.now()
    tt = t2-t1
    print ("%i candles fetched in %s"%(len(candles), str(tt)))
    return candles
    #write_candles(candles)

def get_candle_pandas():
    candles = fetch()

    closes = list()
    COL_CLOSE = 'close'
    COL_VOLUME = 'volume'

    from numpy import array
    closes = [float(z[COL_CLOSE]) for z in candles]
    volumes = [float(z[COL_VOLUME]) for z in candles]
    dates = [z['timestamp'] for z in candles]

    raw_data = {'close': closes, 'volume': volumes}

    df = pd.DataFrame(raw_data, index=dates, columns = ['close', 'volume'])
    return df    

def write():
    df = get_candle_pandas()    
    print (df)
    df.to_csv("bitmex_candles1.csv")

#write()

s3_client = boto3.client('s3')
bucket_name = 'crypto-marketdata'

#aws s3api create-bucket --bucket crypto-marketdata

def put_s3_public(bucket_name, obj_key, data):
    print ("put ", bucket_name)
    s3_client.put_object(Bucket=bucket_name,Key=obj_key,Body = json.dumps(data))
    s3 = boto3.resource('s3')
    object = s3.Bucket(bucket_name).Object(obj_key)
    object.Acl().put(ACL='public-read')

    #bucket.upload_file(file, key, ExtraArgs={'ACL':'public-read'})

    location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    print ("?? ", location)
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, obj_key)
    print ("put to url ",url)

def upload():
    df = pd.read_csv("bitmex_candles1.csv")
    df['change'] = df['close'].diff()
    df['roc'] = df['change']/df['close']
    df['Quantile_rank']=pd.qcut(df['roc'],4,labels=False)

    print (df)
    
    df['roc'].plot()
    key = "bitmex_minute"
    

    #with open('temp.json', 'w') as f:
    candle_json = df.to_json(orient='records', lines=True)
    #f.write(df.to_json(orient='records', lines=True))
    key = "bitmex_history_0404"
    put_s3_public(bucket_name, key, candle_json)  

if __name__=='__main__':
    write()
    #upload()
    #bn = 'crypto-marketdata'
    #location = boto3.client('s3').get_bucket_location(Bucket=bn)
    #print (location)
    #s3 = boto3.resource('s3')
    #my_bucket = s3.Bucket(bn)
    #http://crypto-marketdata.s3-website-us-east-1.amazonaws.com/

    #print (my_bucket.get_location())

    #for key in conn.list_objects(Bucket=bn)['Contents']:
    #    print(key['Key'])
    
    #s3_client.create_bucket(Bucket='crypto-marketdata', CreateBucketConfiguration={
    #'LocationConstraint': 'eu-west-1'})

    #aws s3api create-bucket --bucket my-cool-bucket --acl public read --region eu-west-1
