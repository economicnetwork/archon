
CRYPTOPIA = 0
BITTREX = 1
KUCOIN = 2
BINANCE = 3
KRAKEN = 4
HITBTC = 5

NAMES = {CRYPTOPIA:"Cryptopia",BITTREX:"Bittrex",KUCOIN:"Kucoin",BINANCE:"Binance",KRAKEN:"Kraken",HITBTC:"Hitbtc"}

CRYPTOPIA_NAME = "Cryptopia"
BITTREX_NAME = "Bittrex"
KUCOIN_NAME = "Kucoin"
BINANCE_NAME = "Binance"
KRAKEN_NAME = "Kraken"
HITBTC_NAME = "Hitbtc"
#supported_exchanges = [CRYPTOPIA,BITTREX,KUCOIN,BINANCE,KRAKEN,HITBTC]
supported_exchanges = [CRYPTOPIA,BITTREX,KUCOIN]

names_arr = [CRYPTOPIA_NAME,BITTREX_NAME,KUCOIN_NAME,BINANCE_NAME,KRAKEN_NAME,HITBTC_NAME]
#supported_exchanges = [CRYPTOPIA,BITTREX]

def get_id(name):    
    try:
        return names_arr.index(name.title())
    except:
        print ("exchange does not exist %s"%name)

