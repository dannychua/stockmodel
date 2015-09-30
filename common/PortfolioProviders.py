# -*- coding: utf-8 -*-

import GlobalConstant
from QTimeSeries import QTimeSeries
from Portfolio import Portfolio
from PortfolioProvider import PortfolioProvider
import pandas as pd

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
        sqlQuery = """
            select S_CON_WINDCODE StockID, TRADE_DT Date, I_WEIGHT Weight
            from WINDDB.DBO.AINDEXHS300FREEWEIGHT
            where S_INFO_WINDCODE = '000016.SH' and TRADE_DT > '%s'
            order by TRADE_DT
            """.format(GlobalConstant.TestStartDate)
        
        # Group SQL result by 'Date', aggregating into list of {StockID,Weight} dicts
        df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
        df = df.groupby('Date').apply(lambda x: x[['StockID','Weight']].to_dict(orient='records'))
        # print df.head()

        # Create portfolio from time-aggregated Series and add each portfolio to portfolio_ts
        portfolio_ts = QTimeSeries()
        for date, holding in df.iteritems():
            portfolio_ts.Add(date, Portfolio(date, holding))

        closingPx = PortfolioProviders.getClosingPx('000016.SH')
        a50PP = PortfolioProvider('A50Index', portfolio_ts, 'A50 index', closingPx)
        return a50PP


    @staticmethod
    def getZhongZheng500():
        pass


    @staticmethod
    def getZhongZheng800():
        pass


    @staticmethod
    def getClosingPx(idxWindID):
        pass


    @staticmethod
    def fetchInBatches(conn, rs, batchCount, maxrows):
        pass





# print PortfolioProviders.getA50()