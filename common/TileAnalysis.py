import datetime as datetime
import numpy as np
from Utils import Str2Date
from PortfolioProviders import PortfolioProviders
from ReturnSeries import ReturnSeries
from Factor import Factor
import Factorlib.BPCalc
import Stock
from QTimeSeries import QTimeSeries
import PortfolioProvider


class TileAnalysis:
    """ The tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
        and then construct tile portfolios for each tile either equally or cap-weighted.
        analyze the time series returns of each tile portfolio
    """

    def __init__(self, dates, univPP, numTiles=5):
        if len(dates) and type(dates[0]) is str:
            self.__dates = [Str2Date(d) for d in dates]
        self.__univPP = univPP
        self.__numTiles = numTiles

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
            scores = np.zeros(len(stockIDs))
            for j in range(len(stockIDs)):
                scores[j] = factor.GetScore(stockIDs, dt, True)

            # Find fraction of scores that are np.nan
            numNans = np.sum(np.isnan(scores))
            fracNans = numNans / float(len(scores))
            try:
                if fracNans > 0.5:
                    raise ValueError('Half of stocks have NaN scores')
            except ValueError as e:
                print 'Error: ', e

            scoreSortIdx = np.argsort(scores)  # sort ascend or descend ??; is NaN on the top or down the bottom?

            # Initialize lists of stock returns
            numStocksInTile = np.floor(len(scores) / float(self.__numTiles))
            topTileStkRets = np.zeros(numStocksInTile)
            botTileStkRets = np.zeros(numStocksInTile)

            for j in range(numStocksInTile):
                topTileStkRets[j] = Stock.ByWindID(stockIDs[scoreSortIdx[j+numNans]]).TotalReturnInRange_Bk(dt, nextDt)
                botTileStkRets[j] = Stock.ByWindID(stockIDs[scoreSortIdx[numStocksInTile-j+1]]).TotalReturnInRange_Bk(dt, nextDt)

            # equal weighted for now, later need to check whether it is cap weighted or equal weighted
            topRet = np.nanmean(topTileStkRets)
            botRet = np.nanmean(botTileStkRets)

            if (bmDemean):
                bmRet = self.__univPP.TotalReturnInRange_Bk(dt, nextDt)
                topRet = topRet - bmRet
                botRet = botRet - bmRet

            topTileRets.Add(nextDt, topRet)
            botTileRets.Add(nextDt, botRet)
            spreads.Add(nextDt, topRet - botRet)

            print(['Top AnnMean, ', str(topTileRets.AnnMean)])
            print(['Top AnnStd,  ', str(topTileRets.AnnStd)])
            print(['Top SR,      ', str(topTileRets.SR)])

            print(['Bot AnnMean, ', str(botTileRets.AnnMean)])
            print(['Bot AnnStd,  ', str(botTileRets.AnnStd)])
            print(['Bot SR,      ', str(botTileRets.SR)])

            print(['Spread AnnMean, ', str(spreads.AnnMean)])
            print(['Spread AnnStd,  ', str(spreads.AnnStd)])
            print(['Spread SR,      ', str(spreads.SR)])




if __name__ == '__main__':
    tileAnalysis = TileAnalysis(['20130101', '20140101', '20150101'], PortfolioProviders.getA50(), 5)
    BP = Factor('BP', 'Book/Price', BPCalc, zz800PP)
    tileAnalysis.run(BP, True)
