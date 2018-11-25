# Internet trading protocol

version 0.01

Internet trading protocol (IXP) defines a unified data and transaction model for all exchanges. Currently all exchanges define their own custom format for balances, orders, transactions and assets. Archon translates any exchange specific data to unified data.
Similar to [FIX](https://en.wikipedia.org/wiki/Financial_Information_eXchange) the benefit of IXP are that exchanges speak the same format and can be used by trading systems, order management systems, portfolio tools, accounting systems, and so on.

There is three types of data:

* exchange specific data in the native format as defined by individual APIs

* unified data translated from exchanges

* global data. data that is aggregated across all exchanges. entries signify which exchange
a piece of data belongs to



## Unified data and API for exchange

Market:

* nominator_denomitor, e.g. LTC_BTC

Open Orders:

tbd

Balances:

[{'symbol': 'BTC','amount': 0.001}]

Transactions:

tbd

Orderbook:

{"bids": [{'quantity': 0.01,'price': 0.1} ...], "asks": [{'quantity': 0.01,'price': 0.2} ...]}

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