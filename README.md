# Archon

General trading framework

* install 

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

* run

python3 example.py

or

```
>>> import archon
>>> abroker = archon.broker.Broker()
>>> arch.setClientsFromFile(abroker)
>>> print(abroker.balance_currency("BTC")['Total'])
```