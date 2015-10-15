import math
import matplotlib.pyplot as plt
import pandas as pd
from QTimeSeries import QTimeSeries



class ReturnSeries(QTimeSeries):
    """Handles a time series of portfolios and the related logic.

        Attributes:
            annMean:            annualized mean
            annStd:             annualized stdev
            sr:                 Sharpe ratio = annualized mean/stdev
            returns:            periodic returns
            compCumReturns:     compound cumulative returns, starting from 1.0
            cumReturns:         non-compound cumulative returns, starting from 0

            __annScalar:        a scalar used to annualize periodic returns

            [To be implemented]
            tStat:              SR*sqrt(numer of years)
            hitRate:            numer of periods with positive returns / number of periods
            maxDrawdown     maximum drawdown
            sortinoRatio:       annualized mean / std(negative returns)
    """

    Dates = None

    def __init__(self, dates, values):
        QTimeSeries.__init__(self, dates, values)
        self.__annScalar = 12.0    # assuming time series is monthly
        self.Dates = dates
        self.__Returns = None
        self.__AnnMean = None
        self.__AnnStd = None
        self.__SR = None
        self.__CompCumReturns = None
        self.__CumReturns = None

    def __calc(self):
        """ Calculates various statistics of the portfolio's returns """
        
        if self.Timeseries.shape[0] >= 2:
            daysDelta = int(self.Timeseries.iloc[1] - self.Timeseries.iloc[0])
            if daysDelta == 1 | daysDelta == 3:     # If weekday
                self.__annScalar = 252
            if daysDelta == 7:                      # If weekly
                self.__annScalar = 52
            if daysDelta > 25 & daysDelta < 33:     # If monthly
                self.__annScalar = 12
            if daysDelta > 85 & daysDelta < 95:     # If quarterly
                self.__annScalar = 4

            # Calculate statistics
            mean = self.Timeseries.mean()
            std = self.Timeseries.std()
            self.__Returns = self.Timeseries.tolist()
            self.__AnnMean = mean * self.__annScalar
            self.__AnnStd = std * self.__annScalar
            self.__SR = math.sqrt(self.__annScalar) * mean / std

            # TODO: need to handle the number of periods in a year
            numPeriods = len(self.__Returns)
            self.__CompCumReturns = self.Timeseries.cumprod()
            self.__CumReturns = self.Timeseries.cumsum()


    def plot(self, type='cr', desc=''):
        """ Plot portfolio's return statistics """
        # Plot Cumulative returns
        if type == 'cr':
            plt.plot(self.Dates, self.CumReturns)
            plt.title(desc, ' Cumulative Returns')

        # Plot Compounding cumulative returns
        elif type == 'ccr':
            plt.plot(self.Dates, self.CompCumReturns)
            plt.title(desc, ' Compounding Cumulative Returns')

        # Plot Returns
        else:
            plt.plot(self.Dates, self.Returns)
            plt.title(desc, ' Returns')

        # TODO: add annotations


    @property
    def AnnMean(self):
        """ Annualized mean """
        if self.__AnnMean is None:
            self.__calc()
        return self.__AnnMean


    @property
    def AnnStd(self):
        """ Annualized stdev """
        if self.__AnnStd is None:
            self.__calc()
        return self.__AnnStd


    @property
    def SR(self):
        """ Sharpe ratio """
        if self.__SR is None:
            self.__calc()
        return self.__SR


    @property
    def Returns(self):
        """ Returns """
        if self.__Returns is None:
            self.__calc()
        return self.__Returns


    @property
    def CompCumReturns(self):
        """ Compound cumulative returns, starting from 1.0 """
        if self.__CompCumReturns is None:
            self.__calc()
        return self.__CompCumReturns


    @property
    def CumReturns(self):
        """ Non-compound cumulative return, starting from 0 """
        if self.__CumReturns is None:
            self.__calc()
        return self.__CumReturns





if __name__ == '__main__':
    returnSeries = ReturnSeries(['20100101', '20100102', '20100103', '20100104'], [111,222,333,444])
    print returnSeries.AnnMean
    print returnSeries.AnnStd
    print returnSeries.SR
    print returnSeries.Returns
    print returnSeries.CompCumReturns