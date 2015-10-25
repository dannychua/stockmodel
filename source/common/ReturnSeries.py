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
            tStat:              AnnSR*sqrt(numer of years)
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
        self.__AnnSR = None
        self.__CompCumReturns = None
        self.__CumReturns = None

    def __calc(self):
        """ Calculates various statistics of the portfolio's returns """
        
        if self.Timeseries.shape[0] >= 2:
            daysDelta = self.Timeseries.index[1] - self.Timeseries.index[0]
            numDays = daysDelta.days
            if numDays == 1 or numDays == 3:     # If weekday
                self.__annScalar = 252
            elif numDays == 7:                      # If weekly
                self.__annScalar = 52
            elif numDays > 25 & numDays < 33:     # If monthly
                self.__annScalar = 12
            elif numDays > 85 & numDays < 95:     # If quarterly
                self.__annScalar = 4
            else:
                raise ValueError('Data frequency unknown: NumDays in the first period: ' + str(numDays))

            # Calculate statistics
            mean = self.Timeseries.mean()
            std = self.Timeseries.std()
            self.__Returns = self.Timeseries.tolist()
            self.__AnnMean = mean * self.__annScalar
            self.__AnnStd = std * math.sqrt(self.__annScalar)
            self.__AnnSR = self.__AnnMean / self.__AnnStd

            self.__CompCumReturns = self.Timeseries.cumprod()  ## wrong !!
            self.__CumReturns = self.Timeseries.cumsum()

            # numPeriods = len(self.dates)
            # obj.CompCumReturns = zeros(numPeriods,1);
            # obj.CumReturns = zeros(numPeriods,1);
            # obj.CompCumReturns(1) = 1+vals(1)*0.01;
            # obj.CumReturns(1) = vals(1);
            # for i=2:numPeriods
            #     obj.CompCumReturns(i) = obj.CompCumReturns(i-1)*(1+vals(i)*0.01);  ## Correct
            #     obj.CumReturns(i) = obj.CumReturns(i-1)+vals(i);
            # end


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
    def AnnSR(self):
        """ Annualized Sharpe ratio """
        if self.__AnnSR is None:
            self.__calc()
        return self.__AnnSR


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
    returnSeries = ReturnSeries(['20100101', '20100102', '20100103', '20100104'], [.1, .2, .3, .4])
    print returnSeries.AnnMean
    print returnSeries.AnnStd
    print returnSeries.AnnSR
    print returnSeries.Returns
    print returnSeries.CompCumReturns
    print returnSeries.CumReturns