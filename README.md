# Archon

General trading and broker framework for Internet/Crypto exchanges

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
