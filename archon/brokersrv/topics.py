"""
topics for middleware
publish and request topics
"""
bitmex_name="bitmex"
deribit_name="deribit"

sub = "sub_"
rep = "rep_"

SUB_TOPIC_ORDERS_BITMEX = sub + 'orders-' + bitmex_name
REP_TOPIC_ORDERS_BITMEX = rep + 'orders-' + bitmex_name

SUB_TOPIC_POS_BITMEX = sub + 'position-' + bitmex_name
REP_TOPIC_POS_BITMEX = rep + 'position-' + bitmex_name

SUB_TOPIC_MARKET_BOOK_BITMEX = sub + 'market-books-' + bitmex_name
REP_TOPIC_MARKET_BOOK_BITMEX = rep + 'market-books-' + bitmex_name

SUB_TOPIC_ORDERS_DERIBIT = sub + 'orders-' + deribit_name
REP_TOPIC_ORDERS_DERIBIT = rep + 'orders-' + deribit_name

SUB_TOPIC_POS_DERIBIT = sub + 'position-' + deribit_name
REP_TOPIC_POS_DERIBIT = rep + 'position-' + deribit_name

SUB_TOPIC_MARKET_BOOK_DERIBIT = sub + 'market-books-' + deribit_name
REP_TOPIC_MARKET_BOOK_DERIBIT = rep + 'market-books-' + deribit_name
