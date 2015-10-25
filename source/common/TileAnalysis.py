from Stock import Stock
from ReturnSeries import ReturnSeries
from Factorlib.WINDIndicators import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class TileAnalysis:
    """ The tile analysis is to put all stocks into equally sized groups and the number of groups is defined by Tile
        and then construct tile portfolios for each tile either equally or cap-weighted.
        analyze the time series returns of each tile portfolio
    """

    def __init__(self, dates, factor, univPP, numTiles=5, bmDemean = True):
        if len(dates) and type(dates[0]) is str:
            self.Dates = [Str2Date(d) for d in dates]
        else:
            self.Dates = dates
        self.Factor = factor
        self.UnivPP = univPP
        self.NumTiles = numTiles
        self.IsBMDemean = bmDemean
        self.ReturnSeriesList = None

    def Run(self):
        try:
            if self.NumTiles < 2:
                raise ValueError('Please specify at least 2 Tiles')
        except ValueError as e:
            print 'Error: ', e
            exit(-1)

        # Initialize ReturnSeries
        periods = len(self.Dates) - 1
        self.ReturnSeriesList = []
        for i in range(self.NumTiles):
            self.ReturnSeriesList.append(ReturnSeries([], [], 'T'+str(i+1)))

        bmRS = ReturnSeries([], [], 'BM')
        spreads_top_bottom = ReturnSeries([], [], 'T1/T'+str(self.NumTiles))
        spreads_top_benchmark =  ReturnSeries([], [], 'T1/BM')
        self.ReturnSeriesList.append(bmRS)
        self.ReturnSeriesList.append(spreads_top_bottom)
        self.ReturnSeriesList.append(spreads_top_benchmark)

        for i in range(periods):
            # Get portfolio and it's stockIDs
            dt = self.Dates[i]
            nextDt = self.Dates[i+1]
            portfolio = self.UnivPP.GetPortfolioAsofFixed(dt, 0)
            stockIDs = portfolio.GetStockIDs()

            # Calculate Factor scores and sort them
            scores = np.zeros(len(stockIDs))
            for j in range(len(stockIDs)):
                scores[j] = self.Factor.GetScore(stockIDs[j], dt, True)

            # Find fraction of scores that are np.nan
            numNans = np.sum(np.isnan(scores))
            fracNans = numNans / float(len(scores))
            try:
                if fracNans > 0.5:
                    raise ValueError('Half of stocks have NaN scores')
            except ValueError as e:
                print 'Error: ', e

            scoreSortIdx = (-scores).argsort() # NaN always in the bottom, this is to sort in a descending order; by defaults ascending order

            '''total non_NaNs: All NaNs in Bottom'''
            numNonNaNStocks = np.count_nonzero(~np.isnan(scores))

            '''Initialize lists of stock returns'''
            numStocksInTile = int(np.floor(numNonNaNStocks / float(self.NumTiles)))

            try:
                if numStocksInTile < 1:
                    raise ValueError('Num of Stocks are fewer than Tiles, please decrease the number of Tiles')
            except ValueError as e:
                print 'Error: ', e
                exit(-1)

            all_tiles_rets = []
            '''NaNs in the bottom'''
            for k in xrange(self.NumTiles):
                tile_rets = []
                for j in xrange(numStocksInTile):
                    tile_rets.append(Stock.ByWindID(stockIDs[scoreSortIdx[j+k*numStocksInTile]]).TotalReturnInRange_VWAP_Bk(dt, nextDt))
                all_tiles_rets.append(tile_rets)

            '''equal weighted for now, later need to check whether it is cap weighted or equal weighted'''
            tile_ret_list = []
            bmRet = self.UnivPP.TotalReturnInRange_Bk(dt, nextDt)
            for idx, ret in enumerate(all_tiles_rets):
                mRet = np.nanmean(ret)
                if self.IsBMDemean:
                    mRet = mRet - bmRet
                tile_ret_list.append(mRet)
                self.ReturnSeriesList[idx].Add(nextDt, mRet)
            bmRS.Add(nextDt, bmRet)
            if len(tile_ret_list):
                spreads_top_bottom.Add(nextDt, tile_ret_list[0] - tile_ret_list[-1])
                if self.IsBMDemean: #already been deducted from ret
                    spreads_top_benchmark.Add(nextDt, tile_ret_list[0])
                else:
                    spreads_top_benchmark.Add(nextDt, tile_ret_list[0] - bmRet)


    def GenReport(self, reportFileName):
        '''
        Generate Tile Return Table Plot.

        Run() must be called before this function. But if not, Run() will be called within the function.,
        :param reportFileName: the pdf file to which the context will be dump
        :return: None
        '''

        if self.ReturnSeriesList is None:
            self.Run()

        ''' Prepare data for Tile Return Table '''
        data = []
        for idx, ret_series in enumerate(self.ReturnSeriesList):
            data.append([ret_series.AnnMean, ret_series.AnnStd, ret_series.AnnSR])

        rowLabels = []
        for rs in self.ReturnSeriesList:
            rowLabels.append(rs.Name)

        colLabels = ['Ann Returns', 'Ann Std', 'Sharp Ratio']

        cell_text = []
        n_rows = len(data)
        for row in xrange(n_rows):
            cell_text.append(['%1.2f' % x for x in data[row]])
        the_table = plt.table(cellText=cell_text,
                              colWidths =[0.15]*len(colLabels),
                              rowLabels=rowLabels,
                              colLabels=colLabels,
                              loc='center')

        plt.yticks([])
        plt.xticks([])
        plt.title('Tile Return Analysis Report')
        pp = PdfPages(reportFileName)
        plt.savefig(pp, format='pdf')
        pp.close()
