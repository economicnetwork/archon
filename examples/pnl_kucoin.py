#date,market,txtype,price,_,amount,_,_,_,fee,_
COL_PRICE = 3
COL_AMOUNT = 4

def arr(x):
    date,market,txtype,price,_,amount,_,_,_,fee,_ = x
    price = float(price)
    amount = float(amount)
    return [date,market,txtype,price,amount]

def get_data():
    #download csv file
    with open('kucoin_trades.csv') as f:
        lines = f.readlines()[1:]
        lines = [x.replace('\n','') for x in lines]
        d = [x.split(',') for x in lines]
        a = [arr(x) for x in d]
        return a

def total(data):
    x = [x[COL_AMOUNT] for x in data]
    return sum(x)

def vwap(data):
    vwap = 0
    t = total(data)
    for b in data:    
        f = b[COL_AMOUNT]/t
        p = b[COL_PRICE]
        vwap += p*f
    return vwap

data = get_data()
#print (data)

buys = list()
sells = list()
for x in data[1:]:
    #['Time', 'Coins', 'Sell/Buy', 'Filled Price', 'Coin', 'Amount', 'Coin', 'Volume', 'Coin', 'Fee', 'Coin']
    [date,market,txtype,price,amount] = x
    if txtype=='BUY':
        buys.append(x)
    else:
        sells.append(x)

eth_usd = 200

tb = total(buys)
ts = total(sells)
open_amount = (tb-ts)

buy_vwap = vwap(buys)
sell_vwap = vwap(sells)

current_price = 0.00059
current = open_amount*current_price

total_cost = buy_vwap*tb
total_value = sell_vwap*ts + current

total_buy_eth = tb*buy_vwap
total_buy_usd = total_buy_eth*eth_usd
pnl = total_value - total_cost
pnl_usd = pnl*eth_usd
roi = pnl/total_buy_eth

print ("total buy %.0f"%tb)
print ("total sell %.0f"%ts)
print ("total buy usd %.0f"%total_buy_usd)
print ("buy_vwap %.8f"%buy_vwap)
print ("sell_vwap %.8f"%sell_vwap)
print ("open %.0f"%open_amount)
print ("total_cost %0.3f"%total_cost)
print ("total_value %0.3f"%total_value)

print ("pnl (eth) %.3f"%pnl)
print ("pnl (usd) %.0f"%pnl_usd)
print ("roi %.1f %%"%(roi*100))
