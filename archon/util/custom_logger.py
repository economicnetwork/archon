import logging
import colorlog
import os

#format="%(asctime)s [%(threadName)-12.12s] [%(filename)-18s] [%(name)s] [%(levelname)-5.5s]  %(message)s",        

#def setup_logger(logger_name, log_file, level=logging.DEBUG):
def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)

    formatter = logging.Formatter('[%(name)s] %(asctime)s : %(message)s')

    logdir = "./log/"
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    fileHandler = logging.FileHandler(logdir + log_file, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

    handler = colorlog.StreamHandler()
    colorformat = colorlog.ColoredFormatter('%(log_color)s[%(name)s] %(message)s - (%(asctime)s) %(lineno)d')
    handler.setFormatter(colorformat)

    l.addHandler(handler)


def remove_loggers():
    verbose_loggers = ["urllib3.util.retry", "urllib3.util", "urllib3", "urllib3.connection", "urllib3.response", "urllib3.connectionpool", "urllib3.poolmanager", "urllib3.contrib.pyopenssl", "urllib3.contrib", "socks", "requests", "websocket", "matplotlib", "matplotlib.ticker", "matplotlib.dates", "asyncio", "asyncio.coroutines", "websockets.server", "websockets", "websockets.protocol", "websocket-client", "requests.packages.urllib3", "requests.packages"]
    ##for key in logging.Logger.manager.loggerDict:
    for key in verbose_loggers:
        logging.getLogger(key).setLevel(logging.WARNING)

def remove_all_loggers():
    verbose_loggers = ["urllib3.util.retry", "urllib3.util", "urllib3", "urllib3.connection", "urllib3.response", "urllib3.connectionpool", "urllib3.poolmanager", "urllib3.contrib.pyopenssl", "urllib3.contrib", "socks", "requests", "websocket", "matplotlib", "matplotlib.ticker", "matplotlib.dates", "asyncio", "asyncio.coroutines", "websockets.server", "websockets", "websockets.protocol", "websocket-client", "requests.packages.urllib3", "requests.packages"]
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.WARNING)

