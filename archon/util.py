import logging
import os


def submit_csv():
    with open('orders.csv','r') as f:
        lines = f.readlines()        
        for l in lines: 
            l = l.replace('\n','')
            arr = l.split(';')
            otype,price,qty = arr[0],float(arr[1]),int(arr[2])
            #ttype,order_price,qty = order
            print (price," ",qty)
            broker.submit_check(arr, single_exchange) 

def bid_order_array(market,p,q,reference_price):
    """ make array of orders from array of percents, quantities and reference price """
    i = 0
    orders = list()
    print ("bid order array. ref: " + str(reference_price))
    print (str(p))
    for px in p:
        submit_price = reference_price * (1-px)
        orders.append([market,"BUY",submit_price,q[i]])
        i+=1
    return orders

def ask_order_array(market,p,q,reference_price):
    """ make array of orders from array of percents, quantities and reference price """
    i = 0
    orders = list()
    for px in p:
        submit_price = reference_price * (1+px)
        orders.append([market,"SELL",submit_price,q[i]])
        i+=1
    return orders


def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def setup_logger(logpath, name, log_file, level=logging.INFO):    
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    
    #logPath = "./"
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logpath, log_file)),
        logging.StreamHandler()
    ])
    formatter = logging.Formatter('%(asctime)s,%(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

def ask_user(question):
    check = str(input(question + " (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

def ask_user_qty():
    check = str(input("Which Quantity")).lower().strip()
    try:
        f = float(check)
        return f
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

def ask_user_price():
    check = str(input("Which Price")).lower().strip()
    try:
        f = float(check)
        return f
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()
