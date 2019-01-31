

def calc_mid_price(book):
    topbid,topask = book['bids'][0],book['asks'][0]
    tbp,tap = topbid['price'],topask['price']
    mid = (tbp + tap)/2
    return mid