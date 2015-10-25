__author__ = 'xiaodan'
import sys, os
from TileAnalysis import TileAnalysis
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Factorlib.WINDIndicators import *
from Factor import Factor
from PortfolioProviders import PortfolioProviders
from ReturnSeries import ReturnSeries
from Stock import Stock
import numpy as np
import matplotlib.pyplot as plt
import GlobalConstant
from matplotlib.backends.backend_pdf import PdfPages


class TileAnalysisReport(TileAnalysis):


    def Report(self, factor, reportFileName, bmDemean=False):
        try:
            if self.NumTiles < 2:
                raise ValueError('Please specify at least 2 Tiles')
        except ValueError as e:
            print 'Error: ', e
            exit(-1)

        # Initialize ReturnSeries
        periods = len(self.Dates) - 1
        allTileRetSeriesList = []
        for i in xrange(self.NumTiles):
            allTileRetSeriesList.append(ReturnSeries([], []))

        spreads_top_bottom = ReturnSeries([], [])
        spreads_top_benchmark =  ReturnSeries([], [])
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
                if bmDemean:
                    mRet = mRet - bmRet
                tile_ret_list.append(mRet)
                allTileRetSeriesList[idx].Add(nextDt, mRet)
            if len(tile_ret_list):
                spreads_top_bottom.Add(nextDt, tile_ret_list[0] - tile_ret_list[-1])
                if bmDemean: #already been deducted from ret
                    spreads_top_benchmark.Add(nextDt, tile_ret_list[0])
                else:
                    spreads_top_benchmark.Add(nextDt, tile_ret_list[0] - bmRet)

        '''
        Prepare data for Tile Return Table
        '''
        data = []
        for idx, ret_series in enumerate(allTileRetSeriesList):
            data.append([ret_series.AnnMean, ret_series.AnnStd, ret_series.AnnSR])
        data.append([spreads_top_bottom.AnnMean, spreads_top_bottom.AnnStd, spreads_top_bottom.AnnSR])
        data.append([spreads_top_benchmark.AnnMean, spreads_top_benchmark.AnnStd, spreads_top_benchmark.AnnSR])


        '''
        Generate Tile Return Table Plot
        '''
        rowLabels = []
        for i in xrange(self.NumTiles):
            rowLabels.append('T'+str(i+1))
        rowLabels.append('T1-BM')
        rowLabels.append('T1-T'+str(self.NumTiles))

        colLabels = ['Ann Returns', 'Ann Std', 'Sharp Ratio']

        y_offset = np.array([0.0] * len(colLabels))
        cell_text = []
        n_rows = len(data)
        for row in xrange(n_rows):
            y_offset = y_offset + data[row]
            cell_text.append(['%1.2f' % x for x in y_offset])
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

# if __name__ == '__main__':
#     tileAnalysis = TileAnalysisReport(['20130101', '20140101', '20150101'], PortfolioProviders.getA50(), 5)
#     aa50, zz800PP = getAllPP()
#     BP = Factor('BP', 'Book/Price', BPCalc, zz800PP)
#     tileAnalysis.Report(factor=BP, reportFileName=GlobalConstant.DATA_DIR+'/TitleReturnAnalysis_demeanBM.pdf', bmDemean=True)
#     tileAnalysis.Report(factor=BP,  reportFileName=GlobalConstant.DATA_DIR+'/TitleReturnAnalysis.pdf', bmDemean=False)
