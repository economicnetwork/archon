# Requirements

* python3
* pip3
* mongo (optional)
* redis (optional)


# Install

git clone https://github.com/economicnetwork/archon.git && cd archon

pip3 install -r requirements.txt

# configuration files

add apikeys.toml, see apikeys_example.toml in $HOME/.archon (mkdir $HOME/.archon first)

```
[exchangename]
public_key = ""
secret = ""
```

add conf.toml with mongo and redis details:

```
[MONGO]
uri = "mongodb://localhost:27017"

[REDIS]
host = "localhost"
port = 6379
```

# testing

see testing and examples folder to try out basic features
