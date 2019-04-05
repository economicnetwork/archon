"""
exchanges. this acts as a routing table
"""

BITMEX = "BITMEX"
DERIBIT = "DERIBIT"
DELTA = "DELTA"
BITTREX = "BITTREX"
KUCOIN = "KUCOIN"
BINANCE = "BINANCE"
KRAKEN = "KRAKEN"
HITBTC = "HITBTC"
CRYPTOPIA = "CRYPTOPIA"
OKEX = "OKEX"

NAMES = [BITMEX, DERIBIT, DELTA, OKEX]

def exchange_exists(name):
    return name in NAMES
