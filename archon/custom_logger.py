import logging

#format="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",        

"""
def setup_logger_old(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('>> [%(name)s] %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler("./log/" + log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler) 
"""

def archon_setup_logger(logger_name, log_file, level=logging.INFO):
    print ("setup ",logger_name)
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(name)s] %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler("./log/" + log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler) 





"""    
class ConsoleHandler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


class FileHandler(logging.FileHandler):

    def __init__(self, file):
        #"{0}/{1}.log".format("./log", "simple")
        logging.FileHandler.__init__(self, file)
        #logging.StreamHandler.__init__(self)
        #fmt = '%(asctime)s %(filename)-18s %(levelname)-8s: %(message)s'
        fmt="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",
        fmt_date = '%Y-%m-%dT%T%Z'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


"""