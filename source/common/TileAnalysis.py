import datetime as datetime
import numpy as np
from Utils import Str2Date
from PortfolioProviders import PortfolioProviders
from ReturnSeries import ReturnSeries
from Factor import Factor
import source.common.Factorlib.WINDIndicators
from Stock import *
from ReturnSeries import *
from QTimeSeries import QTimeSeries
import PortfolioProvider
from Factorlib.WINDIndicators import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from buildFactorCache import getAllPP

class TileAnalysis:
    """ The tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
        and then construct tile portfolios for each tile either equally or cap-weighted.
        analyze the time series returns of each tile portfolio
    """

    def __init__(self, dates, univPP, numTiles=5):
        if len(dates) and type(dates[0]) is str:
            self.Dates = [Str2Date(d) for d in dates]
        else:
            self.Dates = dates
        self.UnivPP = univPP
        self.NumTiles = numTiles



    def Run(self, factor, bmDemean=False):
        # Initialize ReturnSeries
        periods = len(self.Dates) - 1
        topTileRets = ReturnSeries([], [])
        botTileRets = ReturnSeries([], [])
        spreads = ReturnSeries([], [])

        for i in range(periods):
            # Get portfolio and it's stockIDs
            dt = self.Dates[i]
            nextDt = self.Dates[i+1]
            portfolio = self.UnivPP.GetPortfolioAsofFixed(dt, 0)
            stockIDs = portfolio.GetStockIDs()

            # Calculate Factor scores and sort them
            scores = np.zeros(len(stockIDs))
            for j in range(len(stockIDs)):
                scores[j] = factor.GetScore(stockIDs[j], dt, True)

            # Find fraction of scores that are np.nan
            numNans = np.sum(np.isnan(scores))
            fracNans = numNans / float(len(scores))
            try:
                if fracNans > 0.5:
                    raise ValueError('Half of stocks have NaN scores')
            except ValueError as e:
                print 'Error: ', e

            #scoreSortIdx = np.argsort(scores)  # sort ascend or descend ??; is NaN on the top or down the bottom?
            scoreSortIdx = (-scores).argsort() # NaN always in the bottom, this is to sort in a descending order; by defaults ascending order

            #total non_NaNs: All NaNs in Bottom
            numNonNaNStocks = np.count_nonzero(~np.isnan(scores))

            # Initialize lists of stock returns
            numStocksInTile = int(np.floor(numNonNaNStocks / float(self.NumTiles)))
            topTileStkRets = np.zeros(numStocksInTile)
            botTileStkRets = np.zeros(numStocksInTile)

            ## assuming nans are on the top !!!! need to be tested!!!
            for j in range(numStocksInTile):
                topTileStkRets[j] = Stock.ByWindID(stockIDs[scoreSortIdx[j]]).TotalReturnInRange_VWAP_Bk(dt, nextDt)
                botTileStkRets[j] = Stock.ByWindID(stockIDs[scoreSortIdx[-j-1]]).TotalReturnInRange_VWAP_Bk(dt, nextDt)

            # equal weighted for now, later need to check whether it is cap weighted or equal weighted
            topRet = np.nanmean(topTileStkRets)
            botRet = np.nanmean(botTileStkRets)

            if bmDemean:
                bmRet = self.UnivPP.TotalReturnInRange_Bk(dt, nextDt)
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
    aa50, zz800PP = getAllPP()
    BP = Factor('BP', 'Book/Price', BPCalc, zz800PP)
    tileAnalysis.Run(BP, True)
