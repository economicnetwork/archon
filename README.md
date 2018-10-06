# Archon

General trading and broker framework for Internet/Crypto exchanges

The framework interacts with the exchanges through the API keys for the purpose of 

* tracking assets
* order-execution
* exchange functionality indepedent from web-view 

It abstracts from exchanges in that datastructures are generic for all exchanges

Ecosystem which can be built on top

* Multi-Exchange trading interface
* Streaming service
* Bot and strategy framework
* ...

Currently in alpha

## examples

balance_all.py - send balance report via mail 

order.py - submit order example

cancel.py - cancel open order by command line

user_tx.py - user transactions

## install 

needs python3 
pip3 install -r requirements.txt

add apikeys.toml, see apikeys_example.toml

```
[apikeys.exchangename]
public_key = ""
secret = ""
```

add conf.toml with mailgun key and mongo details (see example_conf.toml)


