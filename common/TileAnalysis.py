import datetime as datetime
from Utils import Str2Date
from PortfolioProviders import PortfolioProviders
from ReturnSeries import ReturnSeries


class TileAnalysis:
	""" The tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
		and then construct tile portfolios for each tile either equally or cap-weighted.
		analyze the time series returns of each tile portfolio
	"""

	def __init__(self, dates, univPP, numTiles=5):
		if len(dates) and type(dates[0]) is str:
			self.__dates = [Str2Date(d) for d in dates]
		self.__univPP = univPP


	def run(self, factor=None, bmDemean=False):
		# Initialize ReturnSeries
		periods = len(self.__dates) - 1
		topTileRets = ReturnSeries([], [])
		botTileRets = ReturnSeries([], [])
		spreads = ReturnSeries([], [])

		# Force factor to exist for bmDemean to be True
		if(factor and (bmDemean == True)):
			bmDemean = True

		for i in range(periods):
			# Get portfolio and it's stockIDs
			dt = self.__dates[i]
			nextDt = self.__dates[i+1]
			portfolio = self.__univPP.GetPortfolioAsofFixed(dt, 0)
			stockIDs = portfolio.GetStockIDs()

			# Calculate Factor scores and sort them
			scoresList = []
			for j in range(len(stockIDs)):
				score = factor.getScore(stockIDs, dt, 1, True)
				scoresList.append(score)

			# Sort scoresList so NaN scores are on top
			# TODO: Finish up TileAnalysis.Run()





if __name__ == '__main__':
	tileAnalysis = TileAnalysis(['20130101', '20140101', '20150101'], PortfolioProviders.getA50(), 5)
	tileAnalysis.run('someFactor', True)