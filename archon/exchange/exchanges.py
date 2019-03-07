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

NAMES = [BITMEX, DERIBIT, DELTA]

def exchange_exists(name):
    return name in NAMES
