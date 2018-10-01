""" unified model """

import archon.exchange.exchanges as exc
import archon.markets as markets
import archon.tx as atx
import datetime
import pytz

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

def o_key_id(exchange):
    if exchange==exc.CRYPTOPIA:
        return "OrderId"
    elif exchange==exc.BITTREX:
        return "OrderUuid"

def otype_key(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Type"
    elif exchange==exc.BITTREX:
        return "OrderType"

def otype_key_buy(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Buy"
    elif exchange==exc.BITTREX:
        return "LIMIT_BUY"

def otype_key_sell(exchange):
    if exchange==exc.CRYPTOPIA:
        return "Sell"
    elif exchange==exc.BITTREX:
        return "LIMIT_SELL"

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

def bid_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "BidPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Bid"    
    elif exchange==exc.KUCOIN:
        return "buy"    

def ask_key(exchange):
    if exchange==exc.CRYPTOPIA:
        key = "AskPrice"
        return key
    elif exchange==exc.BITTREX:
        return "Ask"
    elif exchange==exc.KUCOIN:
        return "sell"    

def conv_usertx(tx, exchange):
    if exchange==exc.CRYPTOPIA:
        r = tx['Rate']
        a = tx['Amount']
        ty = tx['Type']
        m = tx['Market']
        ts = tx['TimeStamp'][:19]
        dt = atx.conv_timestamp_tx(ts,exchange)
        d = {'price':r,'quantity':a,'txtype':ty,'market':m,'timestamp':dt}
        return d

    elif exchange==exc.BITTREX:
        t = tx['TimeStamp']
        #2018-09-10T17:07:44.507
        dt = atx.conv_timestamp(t,exchange)
        p = tx['Limit']
        q = tx['Quantity']
        d = {'price':p,'quantity':q,'timestamp':dt} #,'txtype':ty,'market':m,'timestamp':timestamp_from}
        return d


def conv_timestamp_tx(ts, exchange):    
    if exchange==exc.CRYPTOPIA:
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
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
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)


def conv_timestamp(ts, exchange):    
    if exchange==exc.CRYPTOPIA:
        #local = pytz.timezone("Europe/London") 
        #tsf = datetime.datetime.fromtimestamp(ts)
        tsf = datetime.datetime.utcfromtimestamp(ts)        
        #local_dt = local.localize(tsf, is_dst=None)
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        #dt = utc_dt.strftime(date_broker_format)        
        
        return utc_dt
    elif exchange==exc.BITTREX:
        ts = ts.split('.')[0]
        tsf = datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S')
        utc=pytz.UTC
        utc_dt = tsf.astimezone(pytz.utc)
        utc_dt = utc_dt + datetime.timedelta(hours=4)
        return utc_dt

def convert_tx(tx, exchange, market):
    """ convert transaction """
    if exchange==exc.CRYPTOPIA:
        #CET time        
        ts = tx['Timestamp']
        dt = conv_timestamp(ts, exchange)
        #print (ts,dt)
        ty = tx['Type']
        p = tx['Price']
        market = tx['Label']
        conv_market = markets.convert_markets_to(market, exchange)
        #print (conv_market)
        d = {'timestamp': dt, 'txtype': ty,'price':p,'exchange':exchange,'market':conv_market}
        return d
    elif exchange==exc.BITTREX:
        #UTC time
        ts = tx['TimeStamp']
        dt = conv_timestamp(ts, exchange)
        ty = convert_type_key(tx['OrderType'], exchange)
        p = tx['Price']
        d = {'timestamp': dt, 'txtype': ty,'price':p,'exchange':exchange,'market':market}
        return d
    elif exchange==exc.KUCOIN:
        ts,ty,p,qty,total,txid = tx
        dt = conv_timestamp(ts, exchange)
        #[1538390455000, 'SELL', 2.94e-06, 60.0, 0.0001764, '5bb1f9b6a07e5d75b084ae19']
        d = {'timestamp': dt, 'txtype': ty,'price':p,'exchange':exchange,'market':market}
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
    if exchange==exc.CRYPTOPIA:
        pair = m['Label']
        market = markets.convert_markets_to(pair,exchange)
        bid = m['BidPrice']
        ask = m['AskPrice']
        volume = m['BaseVolume']
        d = {'pair':market,'bid':bid,'ask':ask,'volume':volume}
        return d
    elif exchange==exc.BITTREX:
        # 'Last': 5.6e-07, 'BaseVolume': 1.42803274, 'TimeStamp': '2018-10-01T08:38:19.217', 'Bid': 5.6e-07, 'Ask': 5.7e-07, 'OpenBuyOrders': 140, 'OpenSellOrders': 617, 'PrevDay': 5.3e-07, 'Created': '2016-05-16T06:44:15.287'}
        #print (m)
        pair = m['MarketName']        
        market = markets.convert_markets_to(pair,exchange)
        bid = m['Bid']
        ask = m['Ask']
        high = m['High']
        low = m['Low']
        last = m['Last']
        volume = m['BaseVolume']
        d = {'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':exchange}
        return d
    elif exchange==exc.KUCOIN:
        #{'coinType': 'QSP', 'trading': True, 'symbol': 'QSP-ETH', 
        # 'lastDealPrice': 0.0001569, 'buy': 0.0001497, 'sell': 0.0001569, 
        # #'change': -6.1e-06, 'coinTypePair': 'ETH', 'sort': 0, 
        # #'feeRate': 0.001, 'volValue': 2.61055065, 'high': 0.000157,
        #  'datetime': 1538417238000, 'vol': 17420.292237, 'low': 0.0001426, 
        # 'changeRate': -0.0374}}
        try:
            #print (m)
            pair = m['symbol']
            x,y = pair.split('-')
            market = x + "_" + y
            #market = markets.convert_markets_to(pair,exchange)
            bid = m['buy']
            ask = m['sell']
            high = m['high']
            low = m['low']
            last = m['lastDealPrice']
            volume = m['volValue']            
            d = {'exchange':exchange,'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':exchange}
            return d
        except Exception as err:
            #print ("!",err)
            return {}
    elif exchange==exc.HITBTC:
        #{'ask': '0.0023110', 'bid': '0.0021000', 'last': '0.0023411', 
        # 'open': '0.0027753', 'low': '0.0017000', 'high': '0.0029999', 'volume': '9075000',
        #  'volumeQuote': '19015.3803', 'timestamp': '2018-10-01T21:17:44.681Z',
        # # 'symbol': 'CDCCUSD'}
        pair = m['symbol']
        x,y = pair[:3],pair[-3:]
        market = x + "_" + y
        #market = markets.convert_markets_to(pair,exchange)
        bid = m['bid']
        ask = m['ask']
        high = m['high']
        low = m['low']
        volume = m['volumeQuote']   
        last = m['last']         
        d = {'exchange':exchange,'pair':market,'bid':bid,'ask':ask,'volume':volume,'high':high,'low':low,'last':last,'exchange':exchange}
        return d
        


