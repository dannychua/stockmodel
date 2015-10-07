import datetime as datetime
from Utils import Str2Date
import ReturnSeries


class TileAnalysis():
	""" The tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
		and then construct tile portfolios for each tile either equally or cap-weighted.
		analyze the time series returns of each tile portfolio
	"""

	def __init__(self, dates, univPP, numTiles=5):
		if len(dates) and type(dates[0]) is string:
			self.dates = [ Str2Date(d) for d in dates]
		self.univPP = univPP


	def run(self, factor, bmDemean):
		pass