# Crypto Facilities Ltd REST API V3

import archon.exchange.cryptofacilities as cfApi
import datetime

import archon.config as config
from datetime import datetime
apikeys = config.parse_toml("apikeys.toml")

k = apikeys["CRYPTOFACILITIES"]["public_key"]
s = apikeys["CRYPTOFACILITIES"]["secret"]

apiPath = "https://www.cryptofacilities.com/derivatives"
timeout = 20
checkCertificate = True  # when using the test environment, this must be set to "False"

cfPublic = cfApi.cfApiMethods(apiPath, timeout=timeout, checkCertificate=checkCertificate)
cfPrivate = cfApi.cfApiMethods(apiPath, timeout=timeout, apiPublicKey=k, apiPrivateKey=s, \
                               checkCertificate=checkCertificate)

def APITester():
    ##### public endpoints #####  

    # get instruments
    result = cfPublic.get_instruments()
    print("get_instruments:\n", result)

    # get tickers
    result = cfPublic.get_tickers()
    print("get_tickers:\n", result)

    # get order book
    symbol = "FI_XBTUSD_180615"
    result = cfPublic.get_orderbook(symbol)
    print("get_orderbook:\n", result)

    # get history
    """
    symbol = "FI_XBTUSD_180615"  # "FI_XBTUSD_180615", "cf-bpi", "cf-hbpi"
    lastTime = datetime.datetime.strptime("2016-01-20", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfPublic.get_history(symbol, lastTime=lastTime)
    print("get_history:\n", result)
    """

    ##### private endpoints #####

    # get account
    result = cfPrivate.get_accounts()
    print("get_accounts:\n", result)

    # get fills
    #lastFillTime = datetime.strptime("2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    #result = cfPrivate.get_fills(lastFillTime=lastFillTime)
    #print("get_fills:\n", result)

    # get open positions
    result = cfPrivate.get_openpositions()
    print("get_openpositions:\n", result)


def ordering():
    # send limit order
    """
    orderType = "lmt"
    symbol = "FI_XBTUSD_180615"
    side = "buy"
    size = 1
    limitPrice = 1.00
    result = cfPrivate.send_order(orderType, symbol, side, size, limitPrice)
    print("send_order (limit):\n", result)        

    # send limit order with client id
    orderType = "lmt"
    symbol = "FI_XBTUSD_180519"
    side = "buy"
    size = 1
    limitPrice = 1.00
    clientId = "my_client_id"
    result = cfPrivate.send_order(orderType, symbol, side, size, limitPrice,clientOrderId=clientId)
    print("send_order (limit) with client id:\n", result)

    # send stop order
    orderType = "stp"
    symbol = "FI_XBTUSD_180615"
    side = "buy"
    size = 1
    limitPrice = 1.00
    stopPrice = 2.00
    result = cfPrivate.send_order(orderType, symbol, side, size, limitPrice, stopPrice=stopPrice)
    print("send_order (stop):\n", result)

    # cancel order
    order_id = "e35d61dd-8a30-4d5f-a574-b5593ef0c050"
    result = cfPrivate.cancel_order(order_id)
    print("cancel_order:\n", result)

    # cancel all orders of margin account
    result = cfPrivate.cancel_all_orders(symbol="fi_xrpusd")
    print("cancel_all_orders:\n", result)

    # cancel all orders after a minute
    timeout_in_seconds = 60
    result = cfPrivate.cancel_all_orders_after(timeout_in_seconds)
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
    result = cfPrivate.send_batchorder(jsonElement)
    print("send_batchorder:\n", result)

    """

    ## get open orders
    result = cfPrivate.get_openorders()
    print("get_openorders:\n", result)


def withdraw():
    # send xbt withdrawal request
    targetAddress = "xxxxxxxxxx"
    currency = "xbt"
    amount = 0.12345678
    result = cfPrivate.send_withdrawal(targetAddress, currency, amount)
    print("send_withdrawal:\n", result)

    # get xbt transfers
    lastTransferTime = datetime.datetime.strptime("2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfPrivate.get_transfers(lastTransferTime=lastTransferTime)
    print("get_transfers:\n", result)

    # transfer
    fromAccount = "fi_ethusd"
    toAccount = "cash"
    unit = "eth"
    amount = 0.1
    result = cfPrivate.transfer(fromAccount, toAccount, unit, amount)
    print("transfer:\n", result)

if __name__=='__main__':
    APITester()