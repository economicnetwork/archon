""" unified model """

import archon.exchange.exchanges as exc
import archon.markets as markets
import archon.tx as atx
import archon.feeds.cryptocompare as cryptocompare
import datetime
import pytz

#logpath = './log'
#log = setup_logger(logpath, 'model_logger', 'model')

# ---- key names ----

def price_key(exchange):
    if exchange==exc.CRYPTOPIA:
        price_key = "Price"
        return price_key
    elif exchange==exc.BITTREX:
        price_key = "Rate"
        return price_key

def qty_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Volume"
        return key
    elif exchange==exc.BITTREX:
        return "Quantity"

def o_key_price(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Rate"
    elif exchange==exc.BITTREX:
        return "Limit"
    elif exchange==exc.KUCOIN:
        return "price"


def o_key_id(exchange):
    if exchange==exc.CRYPTOPIA:
        return "OrderId"
    elif exchange==exc.BITTREX:
        return "OrderUuid"
    elif exchange==exc.KUCOIN:
        return "oid"
    

def otype_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Type"
    elif exchange==exc.BITTREX:
        return "OrderType"
    elif exchange==exc.KUCOIN:
        return "otype"

def otype_key_buy(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Buy"
    elif exchange==exc.BITTREX:
        return "LIMIT_BUY"
    elif exchange==exc.KUCOIN:
        return "bid"

def otype_key_sell(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Sell"
    elif exchange==exc.BITTREX:
        return "LIMIT_SELL"
    elif exchange==exc.KUCOIN:
        return "ask"

def tx_amount_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Amount"

def book_key_qty(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Volume"
        return key
    elif exchange==exc.BITTREX:
        return "Quantity"

def book_key_price(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "Price"
        return key
    elif exchange==exc.BITTREX:
        return "Rate"
    elif exchange==exc.KUCOIN:
        return "price"

def bid_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "BidPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Bid"    
    elif exchange==exc.KUCOIN:
        return "bid"    

def ask_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "AskPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Ask"
    elif exchange==exc.KUCOIN:
        return "ask"    

def conv_timestamp_tx(ts, exchange):   
    target_format = '%Y-%m-%dT%H:%M:%S' 
    if exchange==exc.CRYPTOPIA:
        tsf = datetime.datetime.utcfromtimestamp(int(ts/1000))
        #tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        tsf = utc_dt.strftime(target_format)
        return tsf
        #utc_dt = utc_dt + datetime.timedelta(hours=4)
        #dt = utc_dt.strftime(date_broker_format)        
        
        return utc_dt
    elif exchange==exc.BITTREX:
        ts = ts.split('.')[0]
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        return utc_dt
    elif exchange==exc.KUCOIN:
        tsf = datetime.datetime.utcfromtimestamp(ts)
        #tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        tsf = utc_dt.strftime(target_format)
        return tsf
        #tsf = utc_dt.strftime('%H:%M:%S')
        #return tsf


def conv_timestamp(ts, exchange):    
    target_format = '%Y-%m-%dT%H:%M:%S'
    if exchange==exc.CRYPTOPIA:
        #local = pytz.timezone("Europe/London") 
        #tsf = datetime.datetime.fromtimestamp(ts)
        tsf = datetime.datetime.utcfromtimestamp(ts)        
        #local_dt = local.localize(tsf, is_dst=None)
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        #dt = utc_dt.strftime(date_broker_format)        
        tsf = utc_dt.strftime(target_format)
        return tsf
    elif exchange==exc.BITTREX:
        ts = ts.split('.')[0]
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        tsf = utc_dt.strftime(target_format)
        return tsf

    elif exchange==exc.KUCOIN:
        #dt = conv_timestamp(t/1000,exchange)
        tsf = datetime.datetime.utcfromtimestamp(ts/1000)
        #tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        #tsf = utc_dt.strftime()
        tsf = utc_dt.strftime(target_format)
        return tsf

def conv_usertx(tx, exchange):
    n = exc.NAMES[exchange]
    if exchange==exc.CRYPTOPIA:
        r = tx['Rate']
        a = tx['Amount']
        ty = tx['Type']
        m = tx['Market']
        ts = tx['TimeStamp'][:19]
        dt = conv_timestamp_tx(ts,exchange)
        d = {'price':r,'quantity':a,'txtype':ty,'market':m,'timestamp':dt}
        return d

    elif exchange==exc.BITTREX:
        t = tx['TimeStamp']
        #2018-09-10T17:07:44.507
        dt = conv_timestamp(t,exchange)
        p = tx['Limit']
        q = tx['Quantity']
        d = {'price':p,'quantity':q,'timestamp':dt} #,'txtype':ty,'market':m,'timestamp':timestamp_from}
        return d

    elif exchange==exc.KUCOIN:
        t = tx['createdAt']
        dt = conv_timestamp(t/1000,exchange)
        #ty = tx['dealDirection']
        ty = tx['direction']
        q = tx['amount']
        p = tx['dealPrice']
        nom = tx['coinType']
        denom = tx['coinTypePair']
        m = nom + "_" + denom        
        d = {'price':p,'quantity':q,'txtype':ty,'market':m,'timestamp':dt,'exchange':n}
        return d

def conv_tx(tx, exchange, market):
    """ convert transaction """
    if exchange==exc.CRYPTOPIA:
        #CET time        
        ts = tx['Timestamp']
        dt = conv_timestamp(ts, exchange)
        ty = tx['Type']
        if ty == "Buy": 
            ty="BUY"
        else:
            ty="SELL"
        p = tx['Price']
        market = tx['Label']
        conv_market = conv_markets_from(market, exchange)
        d = {'timestamp': dt, 'exchange':exc.NAMES[exchange],'market':conv_market, 'txtype': ty,'price':p,}
        return d
    elif exchange==exc.BITTREX:
        #UTC time
        ts = tx['TimeStamp']
        dt = conv_timestamp(ts, exchange)
        tyt = tx['OrderType']
        qty = tx['Quantity']
        #TODO
        #ty = conv_type_key(tyt, exchange)
        p = tx['Price']
        market = conv_markets_from(market, exchange)
        d = {'timestamp': dt, 'exchange':exc.NAMES[exchange],'market':market, 'txtype': tyt,'price':p,'quantity':qty}
        return d
    elif exchange==exc.KUCOIN:
        ts,ty,p,qty,total,txid = tx
        dt = conv_timestamp(ts, exchange)
        #print (ts,dt)
        #[1538390455000, 'SELL', 2.94e-06, 60.0, 0.0001764, '5bb1f9b6a07e5d75b084ae19']
        market = conv_markets_from(market, exchange)
        d = {'timestamp': dt, 'exchange':exc.NAMES[exchange],'market':market,'txtype': ty,'price':p,'quantity':qty}
        return d

def conv_openorder(order, exchange):    
    if exchange==exc.CRYPTOPIA:
        #[{'': 1885532250, 'TradePairId': 6076, 'Market': 'BOXX/BTC', 
        # 'Type': 'Buy', 'Rate': 2.585e-05, 'Amount': 386.0, 'Total': 0.0099781, 
        # 'Remaining': 386.0, 'TimeStamp': '2018-10-09T07:12:58.997986'}]
        n = exc.NAMES[exchange]
        oid = order['OrderId'] 
        m = order['Market']
        nom = m.split('/')[0]
        denom = m.split('/')[1]
        market = nom + "_" + denom
        if order['Type']=='Buy':
            ty = 'bid' 
        else: 
            ty = 'ask'
        price = order['Rate']
        quantity = order['Total']

        d = {'exchange':n,'oid':oid,'market':market,'quantity':quantity,'price':price,'otype':ty}
        return d

    elif exchange==exc.BITTREX:
        n = exc.NAMES[exchange]
        oid = order['OrderUuid']        
        m = order['Exchange']
        nom = m.split('-')[1]
        denom = m.split('-')[0]
        market = nom + "_" + denom
        price = order['Limit']
        quantity = order['Quantity']
        if order['OrderType']=='LIMIT_BUY':
            ty = 'bid' 
        else: 
            ty = 'ask'

        d = {'exchange':n,'oid':oid,'market':market,'quantity':quantity,'price':price,'otype':ty}

        #[{'Uuid': None, 'OrderUuid': '8f024066-6e2f-4c38-af67-8bb300f1d405', 
        # 'Exchange': 'BTC-BOXX', 'OrderType': 'LIMIT_BUY', 'Quantity': 1522.0, 
        # 'QuantityRemaining': 1522.0, 'Limit': 2.849e-05, 'CommissionPaid': 0.0, 
        # 'Price': 0.0, 'PricePerUnit': None, 'Opened': '2018-10-04T10:37:39.817', '
        # Closed': None, 'CancelInitiated': False, 'ImmediateOrCancel': False,
        #  'IsConditional': False, 'Condition': 'NONE', 'ConditionTarget': None}]
        return d
    elif exchange==exc.KUCOIN: 
        print (order)
        n = exc.NAMES[exchange]
        oid = order['oid']
        #oid = order['userOid']        
        nom = order['coinType']
        denom = order['coinTypePair']
        market = nom + "_" + denom
        if order['direction']=='BUY':
            ty = 'bid' 
        else: 
            ty = 'ask'
        price = order['price']
        #quantity = order['dealAmount']
        quantity = order['pendingAmount']
        #dt = conv_timestamp(ts, exchange)
        #[1538390455000, 'SELL', 2.94e-06, 60.0, 0.0001764, '5bb1f9b6a07e5d75b084ae19']
        d = {'exchange':n,'oid':oid,'market':market,'quantity':quantity,'price':price,'otype':ty}
        return d

    elif exchange==exc.HITBTC:
        #{'id': '62009222739', 'clientOrderId': '12350366', 'symbol': 'ETHBTC', 'side': 'buy', 
        # 'status': 'canceled', 'type': 'limit', 'timeInForce': 'GTC',
        #  'quantity': '0.322', 'price': '0.031058', 'cumQuantity': '0.000', 
        # 'createdAt': '2018-10-09T07:43:47.133Z', 'updatedAt': '2018-10-09T07:49:33.502Z'}
        n = exc.NAMES[exchange]
        oid = order['clientOrderId']
        #oid = order['userOid']        
        market = order['symbol']
        if order['side']=='buy':
            ty = 'bid' 
        else: 
            ty = 'ask'
        price = order['price']        
        quantity = order['quantity']
        #dt = conv_timestamp(ts, exchange)
        #[1538390455000, 'SELL', 2.94e-06, 60.0, 0.0001764, '5bb1f9b6a07e5d75b084ae19']
        d = {'exchange':n,'oid':oid,'market':market,'quantity':quantity,'price':price,'otype':ty}
        return d

def conv_orderbook(book, exchange):
    if exchange==exc.CRYPTOPIA:
        bids = (book["Buy"])
        asks = (book["Sell"])
        rate_key = book_key_price(exchange)
        qty_key =  book_key_qty(exchange)
        newb = list()
        for b in bids:
            newb.append({'price':b[rate_key],'quantity':b[qty_key]})
        newa = list()
        for a in asks:
            newa.append({'price':a[rate_key],'quantity':a[qty_key]})            
        return [newb,newa]
    elif exchange==exc.BITTREX:
        bids = book["buy"]
        asks = book["sell"]
        rate_key = book_key_price(exchange)
        qty_key =  book_key_qty(exchange)
        newb = list()
        for b in bids:
            newb.append({'price':b[rate_key],'quantity':b[qty_key]})
        newa = list()
        for a in asks:
            newa.append({'price':a[rate_key],'quantity':a[qty_key]})            
        return [newb,newa]
    elif exchange==exc.KUCOIN:
        bids = (book["BUY"])
        asks = (book["SELL"])
        newb = list()
        for b in bids:
            p,v,t = b
            d = {'price':p,'quantity':v}
            newb.append(d)
        newa = list()
        for a in asks:
            p,v,t = a
            d = {'price':p,'quantity':v}
            newa.append(d)
        book = [newb,newa]
        return book

def conv_summary(m,exchange):
    n = exc.NAMES[exchange]
    if exchange==exc.CRYPTOPIA:
        pair = m['Label']
        market = conv_markets_from(pair,exchange)
        last = m['LastPrice']
        bid = m['BidPrice']
        ask = m['AskPrice']
        low = m['Low']
        high = m['High']
        volume = m['BaseVolume']
        d = {'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':n}
        return d
    elif exchange==exc.BITTREX:
        # 'Last': 5.6e-07, 'BaseVolume': 1.42803274, 'TimeStamp': '2018-10-01T08:38:19.217', 'Bid': 5.6e-07, 'Ask': 5.7e-07, 'OpenBuyOrders': 140, 'OpenSellOrders': 617, 'PrevDay': 5.3e-07, 'Created': '2016-05-16T06:44:15.287'}
        pair = m['MarketName']        
        market = conv_markets_from(pair,exchange)
        bid = m['Bid']
        ask = m['Ask']
        high = m['High']
        low = m['Low']
        last = m['Last']
        volume = m['BaseVolume']
        d = {'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':n}
        return d
    elif exchange==exc.KUCOIN:
        #{'coinType': 'QSP', 'trading': True, 'symbol': 'QSP-ETH', 
        # 'lastDealPrice': 0.0001569, 'buy': 0.0001497, 'sell': 0.0001569, 
        # #'change': -6.1e-06, 'coinTypePair': 'ETH', 'sort': 0, 
        # #'feeRate': 0.001, 'volValue': 2.61055065, 'high': 0.000157,
        #  'datetime': 1538417238000, 'vol': 17420.292237, 'low': 0.0001426, 
        # 'changeRate': -0.0374}}
        try:
            pair = m['symbol']
            market = conv_markets_from(pair,exchange)
            bid = m['buy']
            ask = m['sell']
            high = m['high']
            low = m['low']
            last = m['lastDealPrice']
            volume = m['volValue']            
            d = {'exchange':exchange,'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':n}
            return d
        except Exception as err:
            print ("!",err)
            return None
    elif exchange==exc.HITBTC:
        #{'ask': '0.0023110', 'bid': '0.0021000', 'last': '0.0023411', 
        # 'open': '0.0027753', 'low': '0.0017000', 'high': '0.0029999', 'volume': '9075000',
        #  'volumeQuote': '19015.3803', 'timestamp': '2018-10-01T21:17:44.681Z',
        # # 'symbol': 'CDCCUSD'}
        try:
            pair = m['symbol']
            x,y = pair[:3],pair[-3:]
            market = x + "_" + y
            market = conv_markets_from(pair,exchange)
            bid = float(m['bid'])
            ask = float(m['ask'])
            high = float(m['high'])
            low = float(m['low'])
            volume = float(m['volumeQuote'])
            last = float(m['last'])
            d = {'exchange':exchange,'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':n}
        except:
            d = None
        return d
        

def conv_balance(b,exchange):
    """ balance: amount, price, USD-value """
    if exchange==exc.CRYPTOPIA:
        newl = list()
        for x in b:
            d = {}
            s = x['Symbol']
            d['symbol'] = s            
            t = float(x['Total'])
            if t > 0:
                #usd_price = cryptocompare.get_usd(s)                
                #print (usd_price,t)
                d['amount'] = t
                #d['USD-value'] = t*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.BITTREX:
        newl = list()
        for x in b:
            d = {}
            s = x['Currency']
            d['symbol'] = s
            t = float(x['Balance'])
            if t > 0:
                #usd_price = get_usd(s)                
                d['amount'] = t
                #d['USD-value'] = t*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.BINANCE:    
        newl = list()
        for x in b:
            s = x['asset']
            f = float(x['free'])
            l = float(x['locked'])        
            if f+l > 0:
                
                d = {}
                d['symbol'] = s
                d['exchange'] = "Binance"            
                d['amount'] = f+l
                #usd_price = get_usd(s)    
                #d['USD-value'] = (f+l)*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.KUCOIN:
        newl = list()
        for x in b:
            s = x['coinType']            
            bb = float(x['balance'])
            fb = float(x['freezeBalance'])
            t = bb+fb
            if t > 0:                
                d = {}            
                d['symbol'] = s
                d['exchange'] = "Kucoin"            
                d['amount'] = t
                #usd_price = get_usd(s)    
                #d['USD-value'] = bb*usd_price
                newl.append(d)
        return newl

    elif exchange==exc.KRAKEN:
        replace_syms = {'XXBT':'BTC','ZEUR':'EUR','ZUSD':'USD'}
        newl = list()
        for k,v in b.items():
            d = {}
            if k in replace_syms.keys():
                k = replace_syms[k]
            d['symbol'] = k
            d['amount'] = v
            newl.append(d)  
        return newl

    elif exchange==exc.HITBTC:
        newl = list()
        """
        for x in ab:
            c = x['currency']
            av = float(x['available'])
            r = float(x['reserved'])
            if av+r > 0:
                blist.append({'currency':c,'total':av+r})
        """
        #TODO add to account
        
        for x in b:
            s = x['currency']
            av = float(x['available'])
            r = float(x['reserved'])
            if av+r > 0:
                d = {}            
                d['symbol'] = s
                d['exchange'] = "Hitbtc"            
                d['amount'] = av+r
                newl.append(d)
        return newl

def conv_candle(history, exchange):
    if exchange==exc.CRYPTOPIA:
        newcandle = list()
        for x in history:
            ts,o,h,l,c = x
            dt = conv_timestamp_tx(ts, exc.CRYPTOPIA)     
            newcandle.append([dt,c])
        return newcandle
    elif exchange==exc.KUCOIN:        
        newcandle = list()
        for x in history:
            ts,o,h,l,c,v = x
            dt = conv_timestamp_tx(ts, exc.KUCOIN)     
            newcandle.append([dt,c])
        return newcandle



def market_from(nom, denom):
    return nom + '_' + denom     

def conv_markets_from(m, exchange):
    if exchange==exc.CRYPTOPIA:
        nom,denom = m.split('/')
        return market_from(nom,denom)
    elif exchange==exc.BITTREX:    
        denom,nom = m.split('-')
        return market_from(nom,denom)
    elif exchange==exc.KUCOIN: 
        nom,denom = m.split('-')
        return market_from(nom,denom)
    elif exchange==exc.HITBTC:
        nom,denom = m[:3],m[-3:]
        return market_from(nom,denom)

def conv_markets_to(m, exchange):
    nom,denom = m.split('_')
    if exchange==exc.BITTREX:        
        return denom + '-' + nom
    elif exchange==exc.CRYPTOPIA: 
        return nom + '_' + denom 
    elif exchange==exc.KUCOIN: 
        return nom + '-' + denom  
    elif exchange==exc.HITBTC: 
        return nom + denom 
     

def get_market(nom,denom,exchange):
    if exchange==exc.BITTREX:        
        return denom + '-' + nom
    elif exchange==exc.CRYPTOPIA: 
        return nom + '_' + denom 
    elif exchange==exc.KUCOIN: 
        return nom + '-' + denom  
    elif exchange==exc.HITBTC: 
        return nom + denom  