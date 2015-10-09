__author__ = 'xiaodan'
# %% header
# % handle a timeseries of portfolios and the related logic
# % date: 7/3/2015
# 
# # %%
# % it is a handle class
import numpy as np
from Utils import Str2Date

class PortfolioProvider:
    # properties
    #     Name                % the ID of the portfolio provider
    #     Description         % the description of the portfolio provider
    #     AvailableDates      % the dates on which a portfolio exist
    #     Portfolios          % the timeseries of portfolios
    #     ClosingPx           % closing price time series, optional, only available for indices
    #     Desc                % description of the portfolio provider
    # end
    
    #% portfolio_ts is a time series of portfolio
    def __init__(self, name, portfolios, desc=None, closingPx=None):
        self.Name = name
        self.__Portfolios = portfolios
        self.__AvailableDates = portfolios.Dates
        self.__Desc = desc
        self.__ClosingPx = closingPx

        
        # % return the portfolio on date if it exists
        # % otherwise return empty
    def GetPortfolioOn(self, date):
        date = Str2Date(date)
        return self.__Portfolios.ValueOn(date)

        # % return the portfolio on dt if it exists
        # % if it doesn't exist, then take the most recent portfolio and don't adjust its weights
        # % if reWeightTo100 is true, re-scale the long side of the portfolio to be 100%
        # % if no portfolio exists before dt, return empty

    def GetPortfolioAsofFixed(self, date, reWeightTo100=0):
        date = Str2Date(date)
        portfolio = self.__Portfolios.ValueAsOf(date)
        if reWeightTo100:
            portfolio.ReWeightTo100()
        return portfolio
        
        # % return the portfolio on dt if it exists
        # % if it doesn't exist, then take the most recent portfolio and carry-over its holdings to date
        # % weights are adjusted to reflect the stock returns from the AsOfDate to date
        # % if reWeightTo100 is true, re-scale the long side of the portfolio to be 100%
        # % if no portfolio exists before dt, return empty
    def GetPortfolioAsof(self, date, reWeightTo100=0):
        date = Str2Date(date)
        portfolio = self.__Portfolios.ValueAsOf(date)
        portfolio.HeldToDate(date, False)
        if reWeightTo100:
            portfolio.ReWeightTo100()
        return portfolio

        
    def TotalReturnInRange(self, startDate, endDate):
        if len(self.__ClosingPx):
            ppRet = np.nan #% to be implemented
        else:
            startValue = self.__ClosingPx.ValueAsOf(startDate)
            endValue = self.__ClosingPx.ValueAsOf(endDate)
            ppRet =100.0*(endValue/startValue - 1.0)
        return ppRet


    def TotalReturnInRange_Bk(self, startDate, endDate):
        if len(self.__ClosingPx):
            ppRet = np.nan  #% to be implemented
        else:
            startValue = self.__ClosingPx.ValueAfter(startDate)
            endValue = self.__ClosingPx.ValueAfter(endDate)
            ppRet = 100.0*(endValue/startValue - 1.0)
        return ppRet

    @property
    def AvailableDates(self):
        return self.__AvailableDates

    @property
    def ClosingPx(self):
        return self.__ClosingPx

    @property
    def Desc(self):
        return self.__Desc

    @property
    def Portfolios(self):
        return self.__Portfolios