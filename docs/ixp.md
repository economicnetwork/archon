# Internet exchange protocol

version 0.01

Internet exchange protocol (IXP) defines a unified transaction model for exchanges. Currently exchanges define their own custom format for clients interacting with their service, i.e. balances, orders, transactions and assets are individual on an exchange level. IXP defines a global standard independent of any particular exchange. Similar to [FIX](https://en.wikipedia.org/wiki/Financial_Information_eXchange) the benefit of IXP is that exchanges can understand the same format and can be used by any trading systems, order management systems, portfolio tools, accounting systems, etc. which interacts with the exchange.

Currently the archon framework translates any exchange specific data to unified data so that the backend 
is a single interface to all exchanges and therefore liquidity in the global marketplace.

There is three types of data:

* exchange specific data in the native format as defined by individual APIs, typically JSON over HTTP

* unified data translated from exchanges

* global data. data that is aggregated across all exchanges. entries signify which exchange a piece of data belongs to

![arch](https://raw.githubusercontent.com/economicnetwork/archon/master/docs/broker.png)


## Unified data for exchanges

Market:

* nominator_denomitor, e.g. LTC_BTC

Open Orders:

[{market: "LTC_BTC", quantity: 0.01, limitprice: 0.1}]

Balances:

[{'symbol': 'BTC','amount': 0.001}]

Transactions:

[{'timestamp': '2018-11-25T01:25:26', 'market': 'LTC_BTC', 'txtype': 'BUY', 'price': 0.00757, 'quantity': 0.3} ...]

Orderbook:

{"bids": [{'quantity': 0.01,'price': 0.1} ...], "asks": [{'quantity': 0.01,'price': 0.2} ...]}

## Broker

A broker understands similar actions as exchanges. Data for requests and actions

Submit Order: 

* order ['LTC_BTC', 'SELL', 0.00522999, 2.0]

Cancel Order:

* by order-id. the Order-management system has to store the order-id

## Global data

Balances

[{'symbol': 'BTC', 'exchange': 'Bittrex', 'amount': 0.001}]

Open orders

[{market: "LTC_BTC", quantity: 0.01, limitprice: 0.1, exchange: "Binance"}]

Orderbook

global orderbook LTC_BTC
{"bids":[{'price': 0.0073866, 'quantity': 0.67615281, 'exchange': 'Cryptopia'}
{'price': 0.00737, 'quantity': 222.9, 'exchange': 'Hitbtc'}
{'price': 0.00736597, 'quantity': 2.699, 'exchange': 'Bittrex'}]
"asks":[{'price': 0.00738697, 'quantity': 90.71, 'exchange': 'Kucoin'}
{'price': 0.00739, 'quantity': 0.35457268, 'exchange': 'Bittrex'}
{'price': 0.00739476, 'quantity': 13.97237, 'exchange': 'Kucoin'}]}

Transactions

[{'timestamp': '2018-11-25T01:25:26', 'exchange': 'Bittrex', 'market': 'LTC_BTC', 'txtype': 'BUY', 'price': 0.00757, 'quantity': 0.3} ...]

