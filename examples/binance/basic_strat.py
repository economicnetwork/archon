"""
basic strategy sub
"""
import time
import archon.broker.broker as broker
import archon.exchange.exchanges as exc

a = broker.Broker(setAuto=False)
a.set_keys_exchange_file(path_file_apikeys="./apikeys.toml")
client = a.afacade.get_client(exc.BINANCE)

def get_balance():
    bal = client.get_account()["balances"]
    d = {}
    for x in bal:
        f,l = float(x["free"]),float(x["locked"])
        a = x["asset"]
        total = f+l
        if total > 0:
            #print (a,total)
            d[a] = total
    return d

def submit_one():
    oo = client.get_open_orders()
    print (oo)
    d = get_balance()
    print (d)

    target_price = '0.00001'
    qty = 1000
    #def submit_order_buy(self, market, quantity, price):
    client.submit_order_buy("BATBTC",qty,target_price)
    time.sleep(1.0)

def show_open():
    oo = client.get_open_orders()
    print (oo)


def cancel_all():
    #cancel all
    oo = client.get_open_orders()
    print (oo)
    for o in oo:
        id = o["orderId"]
        print (id)
        #client.cancel_order(id)
        import pdb
        #pdb.set_trace()
        #client.cancel_order() #o['symbol'],id)
        #params = {"symbol": 'BATBTC',"orderId": "88175781"}
        client.cancel_order(o["symbol"],id)

submit_one()        
show_open()