import toml

def toml_file(fs):
    with open(fs, "r") as f:
        return f.read()

def parse_toml(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def set_keys_exchange(afacade, e, keys):
    pubkey = keys["public_key"]
    secret = keys["secret"]
    afacade.set_api_keys(e,pubkey,secret)