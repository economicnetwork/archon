import broker
import time
import arch
import datetime

from util import *
import mail
import schedule
import time

logpath = '/tmp/log'
log = setup_logger(logpath, 'info_logger', 'arch')
    
def balance_report(abroker):
    """ example of showing balances """
    log.info('*** balances ***\n')
    assets = ['BTC', 'AC3']
    s = "*** balances ***\n"
    for asset in assets:
        v = abroker.balance_currency(asset)['Total']
        log.info('%s => %f'%(asset,v))
        s += '%s => %f\n'%(asset,v)
    print ("send " + str(s))
    mail.send_simple_message(abroker.mail_api_key, abroker.mail_domain, "Balance Report",s)

    """
    #market = "AC3_BTC"
    market = "BOXX_BTC"
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
    """

    
def run_balance_report():
    log.info("run report")
    #logpath = '/tmp/log'
    abroker = broker.Broker()
    arch.setClientsFromFile(abroker)
    balance_report(abroker)        

def schedule_tasks():
    get_module_logger(__name__).info("schedule report")    
    log.info("schedule report")
    schedule.every(10).minutes.do(run_balance_report)    
    #schedule.every().day.at("10:30").do(run_balance_report)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    #schedule.every().hour.do(job)
    

if __name__=='__main__':
    schedule_tasks()
    #run_balance_report()