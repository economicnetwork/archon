
COL_TIME = 0
COL_OPEN = 1
COL_HIGH = 2
COL_LOW = 3
COL_CLOSE = 4

def max_close(candles):
    c = [x[COL_CLOSE] for x in candles]
    return max(c)