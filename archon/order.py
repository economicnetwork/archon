

class Order:

    def __init__(self, *args):
        #market, "BUY", target_price, qty
        self.market = args[0]
        self.otype = args[1]
        self.price = args[2]
        self.qty = args[3]


    """
    def __init__(self, **kwargs):
        
        self.market = kwargs['market']
        self.otype = kwargs['']
        self.price = kwargs['price']
        self.qty = kwargs['qty']
    """
        
    def dict_from_CC(self, d):
        #d ={'market':d['Label'], 'price':d['Price'], }
        pass

    def __str__(self):
        return "%s %s %.8f %.f"%(self.market, self.otype, self.price, self.qty)