
import archon.exchange.exchanges as exc
import archon.facade as facade
import archon.broker as broker

afacade = facade.Facade()
a = broker.Broker()
ae = [exc.HITBTC]
a.set_active_exchanges(ae)
a.set_keys_exchange_file()

b = a.global_balances()
print (b)

#bl = a.get_db().balances.find_one()['balance_items']
#print (bl)


#a.sync_balances()
#b = a.latest_balances()
#print (b)

#TODO in thread
#a.get_db().balances.drop()
#bl = a.global_balances_usd()
#print (bl)    
#a.sync_balances()
