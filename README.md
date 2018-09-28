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
apikey = "key-"
domain = "https://api.mailgun.net/v3/domain/messages"
```

## run

```
>>> import archon
>>> abroker = archon.broker.Broker()
>>> arch.setClientsFromFile(abroker)
>>> print(abroker.balance_currency("BTC")['Total'])
```

## examples

balance_example.py
