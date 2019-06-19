import time
from binance.client import Client # Import the Binance Client
from binance.websockets import BinanceSocketManager # Import the Binance Socket Manager

# Although fine for tutorial purposes, your API Keys should never be placed directly in the script like below. 
# You should use a config file (cfg or yaml) to store them and reference when needed.
PUBLIC = '<YOUR-PUBLIC-KEY>'
SECRET = '<YOUR-SECRET-KEY>'

# Instantiate a Client 
client = Client(api_key=PUBLIC, api_secret=SECRET)

# Instantiate a BinanceSocketManager, passing in the client that you instantiated
bm = BinanceSocketManager(client)

# This is our callback function. For now, it just prints messages as they come.
def handle_message(msg):
    print("price ",msg['p'], " time ", msg['E'])
    #print(msg)

# Start trade socket with 'ETHBTC' and use handle_message to.. handle the message.
#market = 'ETHBTC'
market = 'BTCUSDT'
conn_key = bm.start_trade_socket(market, handle_message)
# then start the socket manager
print ("start stream")
bm.start()

# let some data flow..
time.sleep(5)

# stop the socket manager
bm.stop_socket(conn_key)