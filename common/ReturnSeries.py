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


    def __init__(self, dates, values):
        QTimeSeries.__init__(self, dates, values)
        self.__annScalar = 12.0    # assuming time series is monthly


    def __calc(self):
        """ Calculates various statistics of the portfolio's returns """
        if self.Series.shape[0] >= 2:

            daysDelta = self.Series.iloc[1] - self.Series.iloc[0]
            if daysDelta == 1 | daysDelta == 3:     # If weekday
                self.__annScalar = 252
            if daysDelta == 7:                      # If weekly
                self.__annScalar = 52
            if daysDelta > 25 & daysDelta < 33:     # If monthly
                self.__annScalar = 12
            if daysDelta > 85 & daysDelta < 95:     # If quarterly
                self.__annScalar = 4


            # Calculate statistics
            mean = self.Series.mean()
            std = self.Series.std()
            self.__returns = self.Series.tolist()
            self.__annMean = mean * self.__annScalar
            self.__annStd = std * self.__annScalar
            self.__sr = math.sqrt(self.__annScalar) * mean / std

            # TODO: need to handle the number of periods in a year
            numPeriods = len(self.__returns)
            self.__compCumReturns = self.Series.cumprod()
            self.__cumReturns = self.Series.cumsum()


    def plot(self, type='cr', desc=''):
        """ Plot portfolio's return statistics """
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

        # TODO: add annotations


    @property
    def annMean():
        """ Annualized mean """
        if not hasattr(self, '__annMean'):
            self.__calc()
        return self.__annMean


    @property
    def annStd(self):
        """ Annualized stdev """
        if not hasattr(self, '__annstd'):
            self.__calc()
        return self.__annStd


    @property
    def sr(self):
        """ Sharpe ratio """
        if not hasattr(self, '__sr'):
            self.__calc()
        return self.__sr


    @property
    def returns(self):
        """ Returns """
        if not hasattr(self, '__returns'):
            self.__calc()
        return self.__returns


    @property
    def compCumReturns(self):
        """ Compound cumulative returns, starting from 1.0 """
        if not hasattr(self, '__compCumReturns'):
            self.__calc()
        return self.__compCumReturns


    @property
    def cumReturns(self):
        """ Non-compound cumulative return, starting from 0 """
        if not hasattr(self, '__cumReturns'):
            self.__calc()
        return self.__cumReturns






# returnSeries = ReturnSeries(['20100101', '20100102', '20100103', '20100104'], [1,2,3,4])
# print returnSeries.returns 
# print returnSeries.compCumReturns