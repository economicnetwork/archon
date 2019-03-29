import toml
from pathlib import Path

def toml_file(fs):
    try:
        with open(fs, "r") as f:
            r = f.read() 
            return r           
    except Exception as e:
        raise Exception("toml file not found %s"%str(fs))

def parse_toml(filename):
    toml_string = toml_file(filename)
    parsed_toml = toml.loads(toml_string)
    return parsed_toml

def get_keys(exchange):
    home = str(Path.home())
    api_file = home + "/.archon/apikeys.toml"
    parsed = parse_toml(api_file)
    return parsed[exchange]