import logging

#format="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",        


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

