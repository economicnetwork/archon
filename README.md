# Archon

General trading framework. Exchanges are abstracted as a broker interface
The broker mediates requests from strategies. 

The stack is managed through docker (python, mongo, rabbitmq)

## install 

python3 
pip3 install -r requirements.txt

add apikeys.toml
```
[apikeys.CRYPTOPIA]
public_key = ""
secret = ""
```

add conf.toml

```
apikey = "key-"
domain = "https://api.mailgun.net/v3/domain/messages"
```

## Examples

```
>>> import archon
>>> abroker = archon.broker.Broker()
>>> arch.setClientsFromFile(abroker)
>>> print(abroker.balance_currency("BTC")['Total'])
```

example.py
report.py
