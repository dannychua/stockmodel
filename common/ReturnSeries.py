import matplotlib.pyplot as plt
from QTimeSeries import QTimeSeries



class ReturnSeries(QTimeSeries):
    """Handles a time series of portflios and the related logic.

        Attributes:
        annMean: 			annualized mean
        annStd: 			annualized stdev
        sr:					Sharpe ratio = annualized mean/stdev
        returns:			periodic returns
        compCumReturns:		compound cumulative returns, starting from 1.0
        cumReturns:			non-compound cumulative returns, starting from 1.0

        __annScalar:		a scalar used to annualize periodic returns

        [To be implemented]
        tStat:				SR*sqrt(numer of years)
        hitRate:			numer of periods with positive returns / number of periods
        maxDrawdown:		maximum drawdown
        sortinoRatio:		annualized mean / std(negative returns)

    """


    def __init__(self, dates, values):
        QTimeSeries.__init__(self, dates, values)

        # assuming time series is monthly
        self.__annScalar = 12.0


    def __calc(self):
        self.annMean = 123
        self.annStd = 456


    def plot(self, type='cr', desc=''):
        # Plot Cumulative returns
        if type == 'cr':
            plt.plot(self.dates, self.cumReturns)
            plt.title(desc, ' Cumulative Returns')

        # Plot Compounding cumulative returns
        elif type == 'ccr':
            plt.plot(self.dates, self.compCumReturns)
            plt.title(desc, ' Compounding Cumulative Returns')

        # Plot Returns
        else:
            plt.plot(self.dates, self.returns)
            plt.title(desc, ' Returns')


    @property
    def annMean(self):
        if not hasattr(self, 'annMean'):
            self.__calc()
        return self.annMean


    @property
    def annStd(self):
        if not hasattr(self, 'annstd'):
            self.__calc()
        return self.annStd


    @property
    def sr(self):
        if not hasattr(self, 'sr'):
            self.__calc()
        return self.sr


    @property
    def returns(self):
        if not hasattr(self, 'returns'):
            self.__calc()
        return self.returns


    @property
    def compCumReturns(self):
        if not hasattr(self, 'compCumReturns'):
            self.__calc()
        return self.compCumReturns


    @property
    def cumReturns(self):
        if not hasattr(self, 'cumReturns'):
            self.__calc()
        return self.cumReturns





# returnSeries = ReturnSeries(['2010-01-01', '2010-01-02'], [1,2])
# print returnSeries.annMean, returnSeries.annStd