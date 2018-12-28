# Archon

Trading and broker framework for Internet/Crypto exchanges

Archon makes it simple to trade on multiple exchanges driven by code.

The framework interacts with the exchanges through the API keys for the purpose of 

* all typical exchange functions such as: submitting orders, tracking balances and market prices
* tracking assets, Profit-and-loss statements, strategy analysis
* exchange functionality independent from web-view 

Ecosystem which can be built on top

* Trading bots: arbitrage, market-making, directional trading
* Multi-Exchange trading interface
* Streaming service
* and more

## examples

get global balances ([source](examples/balance_simple.py))

```
a = broker.Broker()
a.set_active_exchanges([exc.BINANCE])
bl = a.global_balances()
print (bl)
```
 
orderbooks ([source](examples/show_ordersbooks.py))
 
```
book = a.afacade.get_orderbook(market,exchange)
name = exc.NAMES[exchange]
display_book(book, name)
```

[balance_all.py](examples/balance_all.py) - send balance report via mail 

[order.py](examples/order.py) - submit order example

[cancel.py](examples/cancel.py) - cancel open order by command line

[user_tx.py](examples/user_tx.py) - user transactions

## simply strategy

[strategy.py](examples/strategy.py) - basic strategy example

## install 

see [install doc](docs/install.md)

API keys - recommended is to limit the keys to disallow withdraws

## Telegram group

https://t.me/joinchat/Dzif7RALfRB98BocX72Z3Q
