# Archon

General trading and broker framework for Internet/Crypto exchanges

The framework interacts with the exchanges through the API keys for the purpose of 

* tracking assets
* order-execution
* exchange functionality indepedent from web-view 

It abstracts from exchanges in that datastructures are generic for all exchanges

## install 

needs python3 
pip3 install -r requirements.txt

add apikeys.toml
```
[apikeys.CRYPTOPIA]
public_key = ""
secret = ""
```

add conf.toml with mailgun key

```
[MAILGUN]
apikey = "key-"
domain = "https://api.mailgun.net/v3/enet.io/messages"
email_from = ""
email_to = ""
```

## examples

balance_all.py - send balance report via mail 

order.py - order example

cancel.py - cancel open order by command line

user_tx.py - user transactions