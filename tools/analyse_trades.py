import broker
import time
import arch
import datetime

from util import *

def analyse(abroker):
    market = "AC3_BTC"
    usertx = abroker.trade_history(market)
    from functools import reduce
    buys = list(filter((lambda x: x['Type'] == 'Buy'),usertx))
    sells = list(filter((lambda x: x['Type'] == 'Sell'),usertx))

    totals_buys = list(map((lambda x: x['Total']), buys))
    totals_sells = list(map((lambda x: x['Total']), sells))
    
    total_buy = reduce( (lambda x, y: x + y), totals_buys)
    total_sell = reduce( (lambda x, y: x + y), totals_sells)

    print ("total buy %.1f"%total_buy)
    print ("total sell %.1f"%total_sell)

    vwap_buy = 0
    for buy in buys:
        vwap_buy += buy['Rate']*buy['Total']/total_buy

    vwap_sell = 0
    for sell in sells:
        vwap_sell += sell['Rate']*sell['Total']/total_sell
    print (vwap_buy)
    print (vwap_sell)


if __name__=='__main__':
    #logpath = '/tmp/log'
    logpath = './log'
    log = setup_logger(logpath, 'info_logger', 'arch')
    abroker = broker.Broker()
    arch.setClientsFromFile(abroker)
    analyse(abroker)
