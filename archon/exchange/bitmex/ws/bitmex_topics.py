
#does not require auth
TOPIC_announcement = "announcement"        #Site announcements
TOPIC_chat = "chat"                #Trollbox chat
TOPIC_connected = "connected"           #Statistics of connected users/bots
TOPIC_funding = "funding"             #Updates of swap funding rates. Sent every funding interval (usually 8hrs)
TOPIC_instrument = "instrument"          #Instrument updates including turnover and bid/ask
TOPIC_insurance = "insurance"           #Daily Insurance Fund updates
TOPIC_liquidation = "liquidation"         #Liquidation orders as they're entered into the book
TOPIC_orderBookL2_25 = "orderBookL2_25"      #Top 25 levels of level 2 order book
TOPIC_orderBookL2 = "orderBookL2"         #Full level 2 order book
TOPIC_orderBook10 = "orderBook10"         #Top 10 levels using traditional full book push
TOPIC_publicNotifications = "publicNotifications" #System-wide notifications (used for short-lived messages)
TOPIC_quote = "quote"               #Top level of the book
TOPIC_quoteBin1m = "quoteBin1m"          #1-minute quote bins
TOPIC_quoteBin5m = "quoteBin5m"          #5-minute quote bins
TOPIC_quoteBin1h = "quoteBin1h"          #1-hour quote bins
TOPIC_quoteBin1d = "quoteBin1d"          #1-day quote bins
TOPIC_settlement = "settlement"          #Settlements
TOPIC_trade = "trade"               #Live trades
TOPIC_tradeBin1m = "tradeBin1m"          #1-minute trade bins
TOPIC_tradeBin5m = "tradeBin5m"          #5-minute trade bins
TOPIC_tradeBin1h = "tradeBin1h"          #1-hour trade bins
TOPIC_tradeBin1d = "tradeBin1d"          #1-day trade bins

#requires auth
TOPIC_affiliate = "affiliate"   # Affiliate status such as total referred users & payout %
TOPIC_execution = "execution"   # Individual executions; can be multiple per order
TOPIC_order = "order"       # Live updates on your orders
TOPIC_margin = "margin"      # Updates on your current account balance and margin requirements
TOPIC_position = "position"    # Updates on your positions
TOPIC_privateNotifications = "privateNotifications" # Individual notifications - currently not used
TOPIC_transact = "transact"     # Deposit/Withdrawal updates
TOPIC_wallet = "wallet"       # Bitcoin address balance data including total deposits & withdrawals

"""
Orderbook topics

orderBook10 pushes the top 10 levels on every tick, but transmits much more data. 
orderBookL2 pushes the full L2 order book, but the payload can get very large.
In the future, orderBook10 may be throttled, so use orderBookL2_25 in any latency-sensitive application. 
For those curious, the id on an orderBookL2_25 or orderBookL2 entry is a composite of price and symbol, 
and is always unique for any given price level. It should be used to apply update and delete actions.

"orderBook10",         // Top 10 levels using traditional full book push
"orderBookL2_25",      // Top 25 levels of level 2 order book
"orderBookL2",         // Full level 2 order book                

sub to orderBookL2 for all levels, or orderBook10 for top 10 levels & save bandwidth
"""