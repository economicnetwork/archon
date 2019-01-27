#!/usr/bin/env python
#https://github.com/danpaquin/coinbasepro-python/blob/master/cbpro/websocket_client.py

# WS client example

import asyncio
import websockets
from websocket import create_connection, WebSocketConnectionClosedException
import json
import time

"""
async def hello():
    async with websockets.connect(
            'wss://ws-feed.pro.coinbase.com') as websocket:
         x = await websocket.recv()
         print (x)

asyncio.get_event_loop().run_until_complete(hello())
"""

url = 'wss://ws-feed.pro.coinbase.com'
ws = create_connection(url)
products = ["BTC-USD"]
sub_params = {'type': 'subscribe', 'product_ids': products}
ws.send(json.dumps(sub_params))

while True:
    data = ws.recv()
    msg = json.loads(data)
    print (msg)
    time.sleep(0.1)
