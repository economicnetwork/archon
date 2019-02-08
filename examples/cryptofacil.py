# Crypto Facilities Ltd REST API V3

import archon.exchange.cryptofacilities as cfApi
import datetime
import time

import archon.config as config
from datetime import datetime
apikeys = config.parse_toml("apikeys.toml")

k = apikeys["CRYPTOFACILITIES"]["public_key"]
s = apikeys["CRYPTOFACILITIES"]["secret"]

timeout = 20

cfclient = cfApi.cfApiMethods(timeout=timeout, apiPublicKey=k, apiPrivateKey=s)

def get_account():
    # get account
    accounts = cfclient.get_accounts()["accounts"]

    #print("get_accounts:\n", accounts)
    #for k,v in accounts.items():
    #    print (k,v)
    cash = accounts["cash"]["balances"]
    print ("cash ",cash)

    margin_account = accounts["fi_xrpusd"]["balances"]
    print ("margin ",margin_account)

def show_instruments():
    instruments = cfclient.get_instruments()["instruments"]
    #print("get_instruments:\n", instruments)
    for v in instruments:
        try:
            if v["tradeable"]:
                s = v["symbol"]
                it = v["type"]
                u = v["underlying"]
                #ti = v["lastTradingTime"]
                print (it,u,s)
        except:
            print ("error",v)

def show_ob():
    
    ob = cfclient.get_orderbook(cfApi.instrument_btc_perp_inv)["orderBook"]
    bids,asks = ob["bids"],ob["asks"]
    for b in bids[:2]:
        print (b)

    for a in asks[:2]:
        print (a)

    COL_PRICE = 0
    COL_QTY = 1
    topbid,topask = bids[0][COL_PRICE],asks[0][COL_PRICE]
    print (topbid,topask)
    spread = (topask-topbid)/topbid
    #print (spread*100)
    #print("get_orderbook:\n", )

def APITester():
    ##### public endpoints #####  

    # get tickers
    result = cfclient.get_tickers()
    print("get_tickers:\n", result)

    # get order book
    symbol = "FI_XBTUSD_180615"
    result = cfclient.get_orderbook(symbol)
    print("get_orderbook:\n", result)

    # get history
    """
    symbol = "FI_XBTUSD_180615"  # "FI_XBTUSD_180615", "cf-bpi", "cf-hbpi"
    lastTime = datetime.datetime.strptime("2016-01-20", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfclient.get_history(symbol, lastTime=lastTime)
    print("get_history:\n", result)
    """

    ##### private endpoints #####

    # get fills
    #lastFillTime = datetime.strptime("2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    #result = cfclient.get_fills(lastFillTime=lastFillTime)
    #print("get_fills:\n", result)

    # get open positions
    result = cfclient.get_openpositions()
    print("get_openpositions:\n", result)


def ordering():
    # send limit order
    """
    orderType = "lmt"
    symbol = "FI_XBTUSD_180615"
    side = "buy"
    size = 1
    limitPrice = 1.00
    result = cfclient.send_order(orderType, symbol, side, size, limitPrice)
    print("send_order (limit):\n", result)        

    # send limit order with client id
    orderType = "lmt"
    symbol = "FI_XBTUSD_180519"
    side = "buy"
    size = 1
    limitPrice = 1.00
    clientId = "my_client_id"
    result = cfclient.send_order(orderType, symbol, side, size, limitPrice,clientOrderId=clientId)
    print("send_order (limit) with client id:\n", result)

    # send stop order
    orderType = "stp"
    symbol = "FI_XBTUSD_180615"
    side = "buy"
    size = 1
    limitPrice = 1.00
    stopPrice = 2.00
    result = cfclient.send_order(orderType, symbol, side, size, limitPrice, stopPrice=stopPrice)
    print("send_order (stop):\n", result)

    # cancel order
    order_id = "e35d61dd-8a30-4d5f-a574-b5593ef0c050"
    result = cfclient.cancel_order(order_id)
    print("cancel_order:\n", result)

    # cancel all orders of margin account
    result = cfclient.cancel_all_orders(symbol="fi_xrpusd")
    print("cancel_all_orders:\n", result)

    # cancel all orders after a minute
    timeout_in_seconds = 60
    result = cfclient.cancel_all_orders_after(timeout_in_seconds)
    print("cancel_order:\n", result)

    # batch order
    jsonElement = {
        "batchOrder":
            [
                {
                    "order": "send",
                    "order_tag": "1",
                    "orderType": "lmt",
                    "symbol": "FI_XBTUSD_180519",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 1.00,
                    "cliOrdId": "my_another_client_id"
                },
                {
                    "order": "send",
                    "order_tag": "2",
                    "orderType": "stp",
                    "symbol": "FI_XBTUSD_180615",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 2.00,
                    "stopPrice": 3.00,
                },
                {
                    "order": "cancel",
                    "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
                },
                {
                    "order": "cancel",
                    "cliOrdId": "my_client_id",
                },
            ],
    }
    result = cfclient.send_batchorder(jsonElement)
    print("send_batchorder:\n", result)

    """

    ## get open orders
    result = cfclient.get_openorders()
    print("get_openorders:\n", result)


def withdraw():
    # send xbt withdrawal request
    targetAddress = "xxxxxxxxxx"
    currency = "xbt"
    amount = 0.12345678
    result = cfclient.send_withdrawal(targetAddress, currency, amount)
    print("send_withdrawal:\n", result)

    # get xbt transfers
    lastTransferTime = datetime.datetime.strptime("2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfclient.get_transfers(lastTransferTime=lastTransferTime)
    print("get_transfers:\n", result)

    # transfer
    fromAccount = "fi_ethusd"
    toAccount = "cash"
    unit = "eth"
    amount = 0.1
    result = cfclient.transfer(fromAccount, toAccount, unit, amount)
    print("transfer:\n", result)

if __name__=='__main__':
    #APITester()
    #get_account()
    #show_instruments()
    while True:
        show_ob()
        time.sleep(5)