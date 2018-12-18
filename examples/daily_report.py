import time
import archon.arch as arch
import archon.facade as facade
from archon.util import *
import archon.mail as mail

import datetime

import schedule
import time

logpath = '/tmp/log'
log = setup_logger(logpath, 'info_logger', 'arch')
    

def order_report():
    """
    market = "LTC_BTC"
    oo = afacade.open_orders(market)
    log.info("open orders " + str(oo))

    txs = afacade.market_history(market)
    log.info("txs " + str(txs[:3]))
    
    for tx in txs[:50]:
        ts = tx['Timestamp']
        tsf = datetime.datetime.fromtimestamp(ts).strftime('%D %H:%M:%S')
        print (tx['Type'],tsf)

    [bids, asks] = afacade.get_orderbook(market)
    log.info("bids " + str(bids[:3]))

    usertx = afacade.trade_history(market)
    print (usertx[:3])
    """

    
def run_balance_report():
    log.info("run report")
    #logpath = '/tmp/log'
    afacade = facade.Facade()
    arch.setClientsFromFile(afacade)
    balance_report(afacade)        

def schedule_tasks():
    get_module_logger(__name__).info("schedule report")    
    log.info("schedule report")
    schedule.every(60*4).minutes.do(run_balance_report)    
    #schedule.every().day.at("10:30").do(run_balance_report)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    #schedule.every().hour.do(job)
    

if __name__=='__main__':
    schedule_tasks()
