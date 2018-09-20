import broker
import time
import arch
import datetime

from util import *

def show(abroker):
    """ example of showing balances """
    log.info('*** balances ***')
    assets = ['BTC', 'AC3']
    for asset in assets:
        v = abroker.balance_currency(asset)['Total']
        log.info('%s => %f'%(asset,v))

    market = "AC3_BTC"    
    oo = abroker.open_orders(market)
    log.info("open orders " + str(oo))

    txs = abroker.market_history(market)
    log.info("txs " + str(txs[:3]))
    
    for tx in txs[:50]:
        ts = tx['Timestamp']
        tsf = datetime.datetime.fromtimestamp(ts).strftime('%D %H:%M:%S')
        print (tx['Type'],tsf)

    [bids, asks] = abroker.get_orderbook(market)
    log.info("bids " + str(bids[:3]))

    usertx = abroker.trade_history(market)
    print (usertx[:3])

if __name__=='__main__':
    #logpath = '/tmp/log'
    logpath = './log'
    log = setup_logger(logpath, 'info_logger', 'arch')
    abroker = broker.Broker()
    arch.setClientsFromFile(abroker)
    while True:
        show(abroker)
        time.sleep(10)
