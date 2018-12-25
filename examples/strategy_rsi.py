"""
rsi strategy
"""

import talib
import numpy as np
import pandas as pd

from backtest import Strategy, Portfolio

import pandas as pd
import archon.facade as facade
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models

import matplotlib.pyplot as plt

a = broker.Broker()
a.set_keys_exchange_file()	

class RSIStrategy(Strategy):
	"""RSI basic strategy"""    
	
	def __init__(self, symbol, bars, buy_barrier, short_barrier):
		"""Requires the symbol ticker and the pandas DataFrame of bars"""
		self.symbol = symbol
		self.bars = bars
		self.buy_barrier = buy_barrier
		self.short_barrier = short_barrier

	def barrier_check_rsi(self, bar):
		""" check signal for every bar. indicators are pre-computed """
		rsi_value = bar['RSI']
		if rsi_value < self.buy_barrier:
			return 1
		elif rsi_value > self.short_barrier: 
			return -1
		else:
			return 0

	def generate_signals(self):
		"""Creates a pandas DataFrame of random signals."""
		signals = pd.DataFrame(index=self.bars.index)
		
		signals['signal'] = self.bars.apply(lambda x: self.barrier_check_rsi(x), axis=1)

		# The first five elements are set to zero in order to minimise
		# upstream NaN errors in the forecaster.
		#signals['signal'][0:5] = 0.0
		return signals

class MarketOnOpenPortfolio(Portfolio):
	"""Inherits Portfolio to create a system that purchases 100 units of 
	a particular symbol upon a long/short signal, assuming the market 
	open price of a bar.

	In addition, there are zero transaction costs and cash can be immediately 
	borrowed for shorting (no margin posting or interest requirements). 

	Requires:
	symbol - A stock symbol which forms the basis of the portfolio.
	bars - A DataFrame of bars for a symbol set.
	signals - A pandas DataFrame of signals (1, 0, -1) for each symbol.	
	"""

	def __init__(self, symbol, bars, signals):
		self.symbol = symbol        
		self.bars = bars
		self.signals = signals
		#self.initial_capital = float(initial_capital)
		self.positions = self.generate_positions()
		self.portfolio = self.bars
		
	def generate_positions(self):
		"""Creates a 'positions' DataFrame that simply longs or shorts
		100 of the particular symbol based on the forecast signals of{1, 0, -1} from the signals DataFrame."""
		positions = pd.DataFrame(index=self.signals.index).fillna(0.0)
		#positions[self.symbol] = 100.0*signals['signal']
		positions[self.symbol] = self.signals['signal']
		return positions
					
	def backtest_portfolio(self):
		"""Constructs a portfolio from the positions DataFrame by 
		assuming the ability to trade at the precise market open price
		of each bar (an unrealistic assumption!). 

		Calculates the total of cash and the holdings (market price of
		each position per bar), in order to generate an equity curve
		('total') and a set of bar-based returns ('returns').

		Returns the portfolio object to be used elsewhere."""

		# Construct the portfolio DataFrame to use the same index
		# as 'positions' and with a set of 'trading orders' in the
		# 'pos_diff' object, assuming market open prices.

		self.portfolio['position'] = self.positions[self.symbol]

		self.bars['position'] = self.positions[self.symbol]
		
		self.portfolio['Pct Change'] = self.bars['close'].astype('float').pct_change()
		baseindex = 100
		self.portfolio['Strategy'] = baseindex * (1 + ( self.bars['position'].shift(1) * self.bars['Pct Change'] )).cumprod()
		self.portfolio['Strategy'][0] = baseindex
		
		#pos_diff = self.positions.diff()
		
		# Create the 'holdings' and 'cash' series by running through
		# the trades and adding/subtracting the relevant quantity from
		# each column
		#portfolio['holdings'] = (self.positions*self.bars[col]).sum(axis=1)
		#portfolio['cash'] = self.initial_capital - (pos_diff*self.bars[col]).sum(axis=1).cumsum()

		# Finalise the total and bar-based returns based on the 'cash'
		# and 'holdings' figures for the portfolio
		#portfolio['total'] = portfolio['cash'] + portfolio['holdings']
		#portfolio['returns'] = portfolio['total'].pct_change()
		return self.portfolio

def plot_portfolio(portfolio):
	ax = plt.gca()
	fig = plt.figure()
	ax1 = fig.add_subplot(311)
	ax1.plot(portfolio['Strategy'])
	ax2 = fig.add_subplot(312)
	ax2.plot(portfolio['Pct Change'],'ro')
	ax3 = fig.add_subplot(313)
	ax3.plot(portfolio['position'],'g')
	plt.show()


def backtest_market(data, buy_barrier, short_barrier, volume_barrier_long, volume_barrier_short):		
	COL_TIME = 0
	COL_CLOSE = 4
	COL_VOLUME = 5
	closes = [x[COL_CLOSE] for x in data]
	dates  = [x[COL_TIME] for x in data]
	volumes = [x[COL_VOLUME] for x in data]

	candle_data = {'close': closes, 'volume': volumes}
	bars = pd.DataFrame(candle_data, index=dates, columns = ['close','volume'])
	#print (bars.describe())
	
	bars['Pct Change'] = bars['close'].astype('float').pct_change()
	bars['RSI'] = talib.RSI(bars['close'])
	bars['volumeROC'] = talib.ROC(bars['volume'])
	
	symbol = market	
	rfs = RSIStrategy('close', bars, buy_barrier, short_barrier, volume_barrier_long, volume_barrier_short)
	signals = rfs.generate_signals()
	#print ("signal summary \n",signals.describe())	

	backtest = MarketOnOpenPortfolio(symbol, bars, signals)
	pf = backtest.backtest_portfolio()	
	lastindex = pf['Strategy'][-1]
	total_return = lastindex/100 -1
	print ("total return ",total_return)

	plot_portfolio(pf)

if __name__ == "__main__":

	currency_to_test = "ADA"
	market = models.market_from(currency_to_test,"BTC")
	daily_data = a.afacade.get_candles_daily(market,exc.BINANCE)
	#daily_data = a.afacade.get_candles_hourly(market,exc.BINANCE)
	buy_barrier = 40
	short_barrier = 60
	backtest_market(daily_data,buy_barrier, short_barrier)
