# -*- coding: utf-8 -*-

import pandas as pd

import GlobalConstant
from QTimeSeries import QTimeSeries
from Portfolio import Portfolio
from PortfolioProvider import PortfolioProvider


class PortfolioProviders():
    """Generates pre-defined portfolio providers.

        since 4/1/2009, the table AIndexHS300FreeWeight has constituents
        and their weights on a daily basis
        before that, the table AIndexMembers has constituents' in-and-out
        dates, and the index can still be constructed using market cap
        
        To validate: 
        1. the boundary of in-and-out dates, i.e., whether the "out" date
        is the first day of being out or the last date of being in.
        2. is it constructed by total market cap or floating market cap?
    """

    @staticmethod
    def getA50():
        """ Create PortfolioProvider for A50 """
        s_info_windcode = '000016.SH'
        return PortfolioProviders.getPortfolioProvider(s_info_windcode, 'A50Index',  'A50 index')


    @staticmethod
    def getZhongZheng500():
        """ Create PortfolioProvider for ZhongZheng500 """
        s_info_windcode = '000905.SH'
        return PortfolioProviders.getPortfolioProvider(s_info_windcode, 'Zhongzheng500',  'Zhongzheng500 index')


    @staticmethod
    def getZhongZheng800():
        """ Create PortfolioProvider for ZhongZheng800 """
        s_info_windcode = '000906.SH'
        return PortfolioProviders.getPortfolioProvider(s_info_windcode, 'Zhongzheng800',  'Zhongzheng800 index')


    @staticmethod
    def getClosingPx(s_info_windcode):
        """ return index closing prices from WIND given the code """

        sqlQuery = """
            select TRADE_DT Date, S_DQ_CLOSE ClosingPx
            from WINDDB.DBO.AIndexEODPrices
            where S_INFO_WINDCODE = '%s' and TRADE_DT > '%s'
            order by TRADE_DT
            """ % (s_info_windcode, GlobalConstant.DataStartDate)

        df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
        #print df.head()  # testing
        dates = df['Date'].tolist()
        closingPx = df['ClosingPx'].tolist()
        return QTimeSeries(dates, closingPx)


    @staticmethod
    def getPortfolioProvider(s_info_windcode, ID, desc=None):
        """ Create PortfolioProvider from WIND given the code """

        sqlQuery = """
            select S_CON_WINDCODE StockID, TRADE_DT Date, I_WEIGHT Weight
            from WINDDB.DBO.AINDEXHS300FREEWEIGHT
            where S_INFO_WINDCODE = '%s' and TRADE_DT > '%s'
            order by TRADE_DT
            """ % (s_info_windcode, GlobalConstant.DataStartDate)

        # Group SQL result by 'Date', aggregating into list of {StockID,Weight} dicts
        df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
        df = df.groupby('Date').apply(lambda x: x[['StockID','Weight']].to_dict(orient='records'))
        #print df.head()  # testing
        # Create portfolio_is
        # - create portfolio from time-aggregated Series and add each portfolio to portfolio_ts
        portfolio_ts = QTimeSeries()
        for date, holding in df.iteritems():
            portfolio_ts.Add(date, Portfolio(date, holding))

        # Create PortfolioProvider from portfolio_ts
        closingPx = PortfolioProviders.getClosingPx(s_info_windcode)
        portfolioprovider = PortfolioProvider(ID, portfolio_ts, desc, closingPx)
        return portfolioprovider


    # TODO: HS300, ??500, CalibrationUniv, ScoringUniv
    # the way to construct HS300, ??500 is similar to A50
    # both CalibrationUniv and ScoringUniv are equal weighted
    # CalibrationUniv is all about filtering out small/illiquid stocks





# portfolio = PortfolioProviders.getA50().GetPortfolioOn('20090401')
# holdings = portfolio.getHoldings()
# print holdings[0]

# print PortfolioProviders.getA50().getAvailableDates()
# print PortfolioProviders.getZhongZheng500()
# print PortfolioProviders.getZhongZheng800()
# print PortfolioProviders.getClosingPx('000016.SH').qseries.iloc[0]