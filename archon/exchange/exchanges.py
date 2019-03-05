
BITMEX = "BITMEX"
DERIBIT = "DERIBIT"
DELTA = "DELTA"
BITTREX = "Bitrex"
KUCOIN = "Kucoin"
BINANCE = "Binance"
KRAKEN = "Kraken"
HITBTC = "Hitbtc"
CRYPTOPIA = "CRYPTOPIA"

NAMES = [BITMEX, DERIBIT, DELTA]

def exchange_exists(name):
    return name in NAMES

"""
def get_id(name):    
    try:
        v = list(NAMES.values())
        return v.index(name)
    except:
        raise Exception("exchange does not exist %s"%name)

"""