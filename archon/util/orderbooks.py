
def aggregate_book(self, books):
    allbids = list()
    allasks = list()
    ts = None
    for z in books:
        b = z['bids']
        allbids += b
        a = z['asks']
        allasks += a
        ts = z['timestamp']
    allbids = sorted(allbids, key=lambda k: k['price'])
    allbids.reverse()
    allasks = sorted(allasks, key=lambda k: k['price'])
    return [allbids,allasks,ts]
