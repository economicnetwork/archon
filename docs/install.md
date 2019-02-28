# Requirements

* python3
* pip3
* mongo (optional)
* redis (optional)


# Install

git clone https://github.com/economicnetwork/archon.git && cd archon

pip3 install -r requirements.txt

# configuration files

add apikeys.toml, see apikeys_example.toml

```
[exchangename]
public_key = ""
secret = ""
```

add conf.toml with mailgun key and mongo details (see example_conf.toml)

# testing

see testing and examples folder to try out basic features
