import logging
import colorlog


#format="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",        

def setup_logger(logger_name, log_file, level=logging.INFO):
    #print ("setup ",logger_name)
    l = logging.getLogger(logger_name)

    formatter = logging.Formatter('[%(name)s] %(asctime)s : %(message)s')

    fileHandler = logging.FileHandler("./log/" + log_file, mode='w')
    fileHandler.setFormatter(formatter)

    #streamHandler = logging.StreamHandler()
    #streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    #l.addHandler(streamHandler) 

    handler = colorlog.StreamHandler()
    colorformat = colorlog.ColoredFormatter('%(log_color)s[%(name)s] %(levelname)s %(asctime)s - %(message)s')
    handler.setFormatter(colorformat)

    #logger = colorlog.getLogger('example')
    l.addHandler(handler)


