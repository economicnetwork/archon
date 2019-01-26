
from bitmex_websocket import BitMEXWebsocket
import logging
from time import sleep
from archon.custom_logger import setup_logger


# Basic use of websocket.
def run():
    setup_logger(logger_name="test", log_file='test.log')
    logger = logging.getLogger("test")

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol="XBTUSD",
                         api_key=None, api_secret=None)

    logger.info("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while(ws.ws.sock.connected):
        logger.info("Ticker: %s" % ws.get_ticker())
        if ws.api_key:
            logger.info("Funds: %s" % ws.funds())
        logger.info("Market Depth: %s" % ws.market_depth())
        logger.info("Recent Trades: %s\n\n" % ws.recent_trades())
        sleep(10)


if __name__ == "__main__":
    run()