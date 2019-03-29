"""
exchanges. this acts as a routing table
"""

BITMEX = "BITMEX"
DERIBIT = "DERIBIT"
DELTA = "DELTA"
BITTREX = "Bitrex"
KUCOIN = "Kucoin"
BINANCE = "Binance"
KRAKEN = "Kraken"
HITBTC = "Hitbtc"
CRYPTOPIA = "CRYPTOPIA"
OKEX = "OKEX"

NAMES = [BITMEX, DERIBIT, DELTA, OKEX]

def exchange_exists(name):
    return name in NAMES
