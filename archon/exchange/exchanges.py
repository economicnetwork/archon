#TODO FIX
 
BITMEX = 1
DERIBIT = 2
DELTA = 3
BITTREX = 4
KUCOIN = 5
BINANCE = 6
KRAKEN = 7
HITBTC = 8
CRYPTOPIA = 99

BITMEX_NAME = "BITMEX"
DERIBIT_NAME = "DERIBIT"
DELTA_NAME = "DELTA"
BITTREX_NAME = "Bitrex"
KUCOIN_NAME = "Kucoin"
BINANCE_NAME = "Binance"
KRAKEN_NAME = "Kraken"
HITBTC_NAME = "Hitbtc"

NAMES = {BITMEX: BITMEX_NAME, DERIBIT: DERIBIT_NAME, DELTA: DELTA_NAME, BITTREX: BITTREX_NAME, KUCOIN: KUCOIN_NAME, BINANCE: BINANCE_NAME, KRAKEN: KRAKEN_NAME, HITBTC: HITBTC_NAME}


def get_id(name):    
    try:
        v = list(NAMES.values())
        #FIX
        return v.index(name)
    except:
        raise Exception("exchange does not exist %s"%name)

