# -*- coding: utf-8 -*-
# %% header
# % this class is to represent a stock
# % Date: 7/3/2015 created
# %       8/1/2015 implemented many properties & methods
#
# %%
# % it is a handle class
import pandas as pd
import numpy as np
import GlobalConstant
from QTimeSeries import QTimeSeries
from SectorIndustry import SectorIndustry
from Utils import Str2Date


class Stock:
    def __init__(self, windID, ticker, shortName, name, exchange, listBoard, listDate):
        # % private because we want to keep only one instance of each Stock
        self.WindID = windID  # Wind stock ID, unique
        self.Ticker = ticker  # ticker used on exchanges
        self.ShortName = shortName  # the short name of the company
        self.Name = name  # the name of the company
        self.Exchange = exchange  # exchange
        self.ListBoard = listBoard  # the list board
        self.ListDate = listDate  # the list date
        self.__AdjClosingPx = None  # adjusted closing prices
        self.__AdjVWAP = None  # adjusted VWAP
        self.__ClosingPx = None  # closing prices
        self.__VolumeShares = None  # trading volume in shares
        self.__VolumeValue = None  # trading volume in thousands of RMB
        self.__FloatingShares = None  # floating shares


        # % ======= to be implemented in the future
        # TradingStatus   % trading status: trading(in Chinese), no trading(in Chinese), XR, XD, N, DR, NULL
        # % sector/industry/daily prices etc ... to be implemented later
        # %DelistDate
        # %Currency
        # % ...

    def getDatafromDB(self):
        sqlString = '''select TRADE_DT, S_DQ_CLOSE, S_DQ_VOLUME, S_DQ_AMOUNT*1000 as S_DQ_AMOUNT, S_DQ_ADJCLOSE, S_DQ_AVGPRICE*S_DQ_ADJFACTOR  as AdjVWAP
                     from WindDB.dbo.ASHAREEODPRICES where S_INFO_WINDCODE = '%s' and S_DQ_TRADESTATUS != '停牌'and TRADE_DT> '%s' order by trade_dt'''
        sqlString = sqlString % (str(self.WindID), str(GlobalConstant.TestStartDate.strftime('%Y%m%d')))
        self.StockDataFrame = pd.read_sql(sqlString, GlobalConstant.DBCONN_WIND)

        # maybe we can utilize the data frame directly without the trouble of so many QTimeSeries objects!!!
        dates = self.StockDataFrame.TRADE_DT.tolist()
        dates = pd.to_datetime(dates, format('%Y%m%d'))
        self.__ClosingPx = QTimeSeries(dates, self.StockDataFrame.S_DQ_CLOSE.tolist())
        self.__VolumeShares = QTimeSeries(dates, self.StockDataFrame.S_DQ_VOLUME.tolist())
        self.__VolumeValue = QTimeSeries(dates, self.StockDataFrame.S_DQ_AMOUNT.tolist())
        self.__AdjClosingPx = QTimeSeries(dates, self.StockDataFrame.S_DQ_ADJCLOSE.tolist())
        self.__AdjVWAP = QTimeSeries(dates, self.StockDataFrame.AdjVWAP.tolist())
        self.StockDataFrame.set_index('TRADE_DT')

    @property
    def ClosingPx(self):
        if not self.__ClosingPx:
            self.getDatafromDB()
        return self.__ClosingPx

    @property
    def VolumeShares(self):
        if not self.__VolumeShares:
            self.getDatafromDB()
        return self.__VolumeShares

    @property
    def VolumeValue(self):
        if not self.__VolumeValue:
            self.getDatafromDB()
        return self.__VolumeValue

    @property
    def AdjClosingPx(self):
        if not self.__AdjClosingPx:
            self.getDatafromDB()
        return self.__AdjClosingPx

    @property
    def AdjVWAP(self):
        if not self.__AdjVWAP:
            self.getDatafromDB()
        return self.__AdjVWAP

    @property
    def FloatingShares(self):
        if not self.__FloatingShares:
            sqlString = '''select TRADE_DT, FLOAT_A_SHR_TODAY*10000 as FloatingShares from WindDB.dbo.ASHAREEODDERIVATIVEINDICATOR
            where S_INFO_WINDCODE = '%s' and TRADE_DT> '%s'  order by trade_dt '''
            sqlString = sqlString % (self.WindID, GlobalConstant.TestStartDate.strftime('%Y%m%d'))  # convert to string first
            df = pd.read_sql(sqlString, GlobalConstant.DBCONN_WIND)
            self.__FloatingShares = QTimeSeries(df.TRADE_DT.tolist(), df.FloatingShares.tolist())  # % value is cell
        return self.__FloatingShares

    def UnAdjPrice(self, date, isAsOf=True):
        if isAsOf:
            return self.ClosingPx.ValueAsOf(date)
        else:
            return self.ClosingPx.ValueOn(date)

    def FloatMarketCap(self, date):
        try:
            mktCap = self.ClosingPx.ValueAsOf(date) * self.FloatingShares.ValueAsOf(date)
            return mktCap
        except:
            return np.nan


    def TotalReturnInRange(self, startDate, endDate):
        '''
        calculate the total return during the period using Adjusted closing prices with AsOf semantics
        if startDate < FirstTradingDate, return None
        if endDate > LastTradingDate (delisted stock) or today, replace endDate as of the most recent date in the price
         series
        :param startDate: the period starts from the AdjClosing price on startDate.AsOf
        :param endDate:  the period ends at endDate.AsOf
        :return: the total return in percentage
        '''
        startDate = Str2Date(startDate)
        endDate = Str2Date(endDate)
        firstDt = self.AdjClosingPx.FirstDate
        if (startDate < firstDt):
            return None
        startValue = self.AdjClosingPx.ValueAsOf(startDate)
        endValue = self.AdjClosingPx.ValueAsOf(endDate)
        return 100.0 * (endValue / startValue - 1.0)


    def TotalReturnInRange_VWAP(self, startDate, endDate):
        '''
        calculate the total return during the period using Adjusted VWAP  with AsOf semantics
        if startDate < FirstTradingDate, return None
        if endDate > LastTradingDate (delisted stock) or today, replace endDate as of the most recent date in the price
         series
        :param startDate: the period starts from the VWAP price on startDate.AsOf
        :param endDate:  the period ends at endDate.AsOf
        :return: the total return in percentage
        '''
        startDate = Str2Date(startDate)
        endDate = Str2Date(endDate)

        firstDt = self.AdjVWAP.FirstDate
        if startDate < firstDt:
            return None

        startValue = self.AdjVWAP.ValueAsOf(startDate)
        endValue = self.AdjVWAP.ValueAsOf(endDate)
        return 100.0 * (endValue / startValue - 1.0)



        # %
        # % when there is no limited up vice versa for selling stocks.
        # %
        # % shall be used in backtest
        # % assume the investment decision is made on startDate
        # % to be conservative:
        # % the entry price is the VWAP on the trading day following startDate
        # % the exit price is the VWAP on the trading day following endDate
        # %
        # %
        # % if startDate < FirstTradingDate, return NaN
        # % if endDate > LastTradingDate (delisted stock) or today, replace
        # % endDate as of the most recent date in the price series
        # % stkReturn is in percentage

    def TotalReturnInRange_VWAP_Bk(self, startDate, endDate):
        #todo: handle limit up/down days: e.g. buy a stock at its limit-up day is difficult
        #todo: confirm that dates when stocks are stop-trading are not in the time series
        '''
        calculate the total return during the period using Adjusted VWAP with NextIfNone semantics
        it is for running backtest conservatively
        NextIfNone: if value on a date exists, return it; otherwise goes to the next data when the data is available
        if startDate < FirstTradingDate, return None
        if endDate > LastTradingDate (delisted stock) or today, replace endDate as of the most recent date in the price
         series
        Be careful when using this method, as it may have unexpected consequence
        :param startDate: the period starts from the VWAP price on startDate.NextIfNone
        :param endDate:  the period ends from the VWAP price on endDate.NextIfNone
        :return: the total return in percentage
        '''
        startDate = Str2Date(startDate)
        endDate = Str2Date(endDate)
        firstDt = self.AdjVWAP.FirstDate
        if startDate < firstDt:
            return None

        if endDate > self.AdjVWAP.LastDate:
            endDate = self.AdjVWAP.LastDate

        startValue = self.AdjVWAP.ValueOn(startDate)
        if startValue is None:
            startValue = self.AdjVWAP.ValueAfter(startDate)

        endValue = self.AdjVWAP.ValueOn(endDate)
        if endValue is None:
            endValue = self.AdjVWAP.ValueAfter(endDate)

        return 100.0 * (endValue / startValue - 1.0)


    def WindIndustryCode(self, date, level=4):
        '''
        :param date: the date of the interest
        :param level: level could be 1,2,3,4, representing the four levels: level 1 is sector, level 4 is the full industry code
        :return: stock's WIND industry code as of date
        '''
        date = Str2Date(date)
        windID = self.WindID
        secInd = SectorIndustry.GetWindIndustry()
        if windID in secInd.keys():
            ts = secInd[windID]
            windIndustryCode = ts.ValueAsOf(date)
            if level <= 3:
                windIndustryCode = windIndustryCode[0:(2 + 2 * level)]
            return windIndustryCode
        else:
            return None


    def WindSectorCode(self, date):
        '''
        the sector code is the four digits of the full industry code. See WIND document for details
        :param date: the date of the interest
        :return: stock's WIND sector code as of date
        '''
        return self.WindIndustryCode(date, 1)

    STOCKMASTERMAP = {}

    @classmethod
    def ByWindID(cls,windID):
        '''
        the only way to initiate a stock.
        Once we map a stock, we cache it in a dictionary
        :param windID: stock WINDID, it is a primary key for stocks in WIND
        :return: Stock instance
        '''
        if windID in cls.STOCKMASTERMAP:
            stock = cls.STOCKMASTERMAP[windID]
        else:
            # % initiate stock properties from database
            sqlString = """select S_INFO_WINDCODE id, S_INFO_CODE Ticker, S_INFO_NAME ShortName, S_INFO_COMPNAME Name,
            S_INFO_EXCHMARKET Exchange, S_INFO_LISTBOARD ListBoard, S_INFO_LISTDATE ListDate
            from WINDDB.DBO.ASHAREDESCRIPTION"""
            df = pd.read_sql(sqlString, GlobalConstant.DBCONN_WIND)
            for row in df.itertuples(True):
                stk = Stock(row[1], row[2], row[3], row[4], row[5], row[6], row[7]) # each row is Series obj, row[0] is the index
                cls.STOCKMASTERMAP[row[1]] = stk
            stock = cls.STOCKMASTERMAP[windID]
        return stock

    #todo: define DefaultInstance, IsDefaultInstance
