from loguru import logger

CRYPTOPIA = 0
BITTREX = 1
KUCOIN = 2
BINANCE = 3
KRAKEN = 4
HITBTC = 5
DERIBIT = 6
BITMEX = 7

NAMES = {CRYPTOPIA:"CRYPTOPIA",BITTREX:"BITTREX",KUCOIN:"KUCOIN",BINANCE:"BINANCE",KRAKEN:"KRAKEN",HITBTC:"HITBTC",DERIBIT:"DERIBIT",BITMEX:"BITMEX"}

supported_exchanges = [CRYPTOPIA,BITTREX,KUCOIN,HITBTC]

def get_id(name):    
    try:
        v = list(NAMES.values())
        return v.index(name)
    except:
        logger.error("exchange does not exist %s"%name)

