"""
{'account': 722235, 'currency': 'XBt', 'riskLimit': 1000000000000, 
'prevState': '', 'state': '', 'action': '', 'amount': 15,
 'pendingCredit': 0, 'pendingDebit': 0, 'confirmedDebit': 0, 
'prevRealisedPnl': -45985, 'prevUnrealisedPnl': 0, 'grossComm': 0, 
'grossOpenCost': 0, 'grossOpenPremium': 0, 'grossExecCost': 0, 
'grossMarkValue': 0, 'riskValue': 0, 'taxableMargin': 0, 'initMargin': 0, 
'maintMargin': 0, 'sessionMargin': 0, 
'targetExcessMargin': 0, 'varMargin': 0, 'realisedPnl': 0, 'unrealisedPnl': 0, 
'indicativeTax': 0, 'unrealisedProfit': 0, 'syntheticMargin': None,
 'walletBalance': 15, 
'marginLeverage': 0, 
'marginUsedPcnt': 0,
 'excessMargin': 15, 
 'excessMarginPcnt': 1, 
'withdrawableMargin': 15, 'timestamp': '2018-11-28T13:30:21.413Z',
 'grossLastValue': 0, 'commission': None}

'marginBalancePcnt': 1,  
"""            

marginBalance = "marginBalance"
walletBalance = "walletBalance"
availableMargin = "availableMargin"


position_description = {
    "account" :  "Your unique account ID",
    "symbol" :  "The contract for this position",
    "currency" :  "The margin currency for this position",
    "underlying" :  "Meta data of the symbol",
    "quoteCurrency" :  "Meta data of the symbol, All prices are in the quoteCurrency",
    "commission" :  "The maximum of the maker, taker, and settlement fee",
    "initMarginReq" :  "The initial margin requirement This will be at least the symbol's default initial maintenance margin, but can be higher if you choose lower leverage",
    "maintMarginReq" :  "The maintenance margin requirement This will be at least the symbol's default maintenance maintenance margin, but can be higher if you choose a higher risk limit",
    "riskLimit" :  "This is a function of your maintMarginReq",
    "leverage" :  "1 / initMarginReq",
    "crossMargin" :  "True/false depending on whether you set cross margin on this position",
    "deleveragePercentile" :  "Indicates where your position is in the ADL queue",
    "rebalancedPnl" :  "The value of realised PNL that has transferred to your wallet for this position",
    "prevRealisedPnl" :  "The value of realised PNL that has transferred to your wallet for this position since the position was closed",
    "currentQty" :  "The current position amount in contracts",
    "currentCost" :  "The current cost of the position in the settlement currency of the symbol (currency)",
    "currentComm" :  "The current commission of the position in the settlement currency of the symbol (currency)",
    "realisedCost" :  "The realised cost of this position calculated with regard to average cost accounting",
    "unrealisedCost" :  "currentCost - realisedCost",
    "grossOpenCost" :  "The absolute value of your open orders for this symbol",
    "grossOpenPremium" :  "The amount your bidding above the mark price in the settlement currency of the symbol (currency)",
    "markPrice" :  "The mark price of the symbol in quoteCurrency",
    "markValue" :  "The currentQty at the mark price in the settlement currency of the symbol (currency)",
    "homeNotional" :  "Value of position in units of underlying",
    "foreignNotional" :  "Value of position in units of quoteCurrency",
    "realisedPnl" :  "The negative of realisedCost",
    "unrealisedGrossPnl" :  "markValue - unrealisedCost",
    "unrealisedPnl" :  "unrealisedGrossPnl",
    "liquidationPrice" :  "Once markPrice reaches this price, this position will be liquidated",
    "bankruptPrice" :  "Once markPrice reaches this price, this position will have no equity",
####
"prevUnrealisedPnl" : "??"
}