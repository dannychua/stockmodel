# %% header
# % this class is to represent a stock
# % Date: 7/3/2015 created
# %       8/1/2015 implemented many properties & methods
#
# %%
# % it is a handle class
import pandas as pd
import GlobalConstant
from QTimeSeries import QTimeSeries
from SectorIndustry import SectorIndustry
from Utils import checkDate

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
        self.AdjClosingPx = None  # adjusted closing prices
        self.AdjVWAP = None  # adjusted VWAP
        self.ClosingPx = None  # closing prices
        self.VolumeShares = None  # trading volume in shares
        self.VolumeValue = None  # trading volume in thousands of RMB
        self.FloatingShares = None  # floating shares


        # % ======= to be implemented in the future
        # TradingStatus   % trading status: trading(in Chinese), no trading(in Chinese), XR, XD, N, DR, NULL
        # % sector/industry/daily prices etc ... to be implemented later
        # %DelistDate
        # %Currency
        # % ...

    def getDatafromDB(self):
        sqlString = '''select TRADE_DT, S_DQ_CLOSE, S_DQ_VOLUME, S_DQ_AMOUNT*1000 as S_DQ_AMOUNT, S_DQ_ADJCLOSE, S_DQ_AVGPRICE*S_DQ_ADJFACTOR  as AdjVWAP
                     from WindDB.dbo.ASHAREEODPRICES where S_INFO_WINDCODE = %s and S_DQ_TRADESTATUS != 'ͣ��'and TRADE_DT> %s order by trade_dt'''
        sqlString = sqlString % (str(self.WindID), str(GlobalConstant.TestStartDate.strftime('%Y%m%d')))
        curs = GlobalConstant.DBCONN_WIND.cursor()
        curs.execute(sqlString)
        rows = curs.fetchall()
        curs.close()
        self.StockDataFrame = pd.DataFrame(rows)
        dates = self.StockDataFrame.TRADE_DT.tolist()
        self.ClosingPx = QTimeSeries(dates, self.StockDataFrame.S_DQ_CLOSE.tolist())
        self.VolumeShares = QTimeSeries(dates, self.StockDataFrame.S_DQ_VOLUME.tolist())
        self.VolumeValue = QTimeSeries(dates, self.StockDataFrame.S_DQ_AMOUNT.tolist())
        self.AdjClosingPx = QTimeSeries(dates, self.StockDataFrame.S_DQ_ADJCLOSE.tolist())
        self.AdjVWAP = QTimeSeries(dates, self.StockDataFrame.AdjVWAP.tolist())
        self.StockDataFrame.set_index('TRADE_DT')

    def getWindID(self):
        return self.WindID

    def getClosingPx(self):
        if not self.ClosingPx:
            self.getDatafromDB()
        return self.ClosingPx

    def getVolumeShares(self):
        if not self.VolumeShares:
            self.getDatafromDB()
        return self.VolumeShares

    def getVolumeValue(self):
        if not self.VolumeValue:
            self.getDatafromDB()
        return self.VolumeValue

    def geAdjClosingPx(self):
        if not self.AdjClosingPx:
            self.getDatafromDB()
        return self.AdjClosingPx

    def getAdjVWAP(self):
        if not self.AdjVWAP:
            self.getDatafromDB()
        return self.AdjVWAP

    def getFloatingShares(self):
        if not self.FloatingShares:
            sqlString = '''select TRADE_DT, FLOAT_A_SHR_TODAY*10000 as FloatingShares from WindDB.dbo.ASHAREEODDERIVATIVEINDICATOR  where S_INFO_WINDCODE = %s and TRADE_DT> %s  order by trade_dt'''
            curs = GlobalConstant.DBCONN_WIND.cursor()
            curs.execute(
                sqlString % (self.WindID, GlobalConstant.TestStartDate.strftime('%Y%m%d')))  # convert to string first
        rows = curs.fetchall()
        curs.close()
        df = pd.DataFrame(rows)
        self.FloatingShares = QTimeSeries(df.TRADE_DT.tolist(), df.FloatingShares.tolist())  # % value is cell
        return self.FloatingShares

    def PriceOnDate(self, date):
        return self.ClosingPx.ValueOn(date)

    def FloatMarketCap(self, date):
        try:
            mktCap = self.ClosingPx.ValueAsOf(date) * self.FloatingShares.ValueAsOf(date)
            return mktCap
        except:
            return None

    # % calculate total returns from startDate to endDate using Adjusted closing prices with asof semantics
    # % if startDate < FirstTradingDate, return NaN
    # % if endDate > LastTradingDate (delisted stock) or today, replace
    # % endDate as of the most recent date in the price series
    # % stkReturn is in percentage

    def TotalReturnInRange(self, startDate, endDate):
        startDate = checkDate(startDate)
        endDate = checkDate(endDate)
        firstDt = self.AdjClosingPx.FirstDate()
        if (startDate < firstDt):
            return None
        startValue = self.AdjClosingPx.ValueAsOf(startDate)
        endValue = self.AdjClosingPx.ValueAsOf(endDate)
        return 100.0 * (endValue / startValue - 1.0)

    # % calculate total returns from startDate to endDate using Adjusted VWAP with asof semantics
    # % if startDate < FirstTradingDate, return NaN
    # % if endDate > LastTradingDate (delisted stock) or today, replace
    # % endDate as of the most recent date in the price series
    # % stkReturn is in percentage

    def TotalReturnInRange_VWAP(self, startDate, endDate):
        startDate = checkDate(startDate)
        endDate = checkDate(endDate)

        firstDt = self.AdjVWAP.FirstDate()
        if startDate < firstDt:
            return None

        startValue = self.AdjVWAP.ValueAsOf(startDate)
        endValue = self.AdjVAWP.ValueAsOf(endDate)
        return 100.0 * (endValue / startValue - 1.0)


        # % to be implemented: handle limit up/down days: e.g. if to buy a
        # % stock which is limited up on the following day, wait for a day
        # % when there is no limited up vice versa for selling stocks.
        # %
        # % shall be used in backtest
        # % assume the investment decision is made on startDate
        # % to be conservative:
        # % the entry price is the VWAP on the trading day following startDate
        # % the exit price is the VWAP on the trading day following endDate
        # % note that if stock stop-trading days should be removed
        # %
        # % if startDate < FirstTradingDate, return NaN
        # % if endDate > LastTradingDate (delisted stock) or today, replace
        # % endDate as of the most recent date in the price series
        # % stkReturn is in percentage

        def totalReturnInRange_Bk(self, startDate, endDate):
            startDate = checkDate(startDate)
            endDate = checkDate(endDate)
            firstDt = self.AdjClosingPx.FirstDate()
            if startDate < firstDt:
                return None

            # %better return the return and the date range, so that the
            # %caller knows how far off the return date range is from the
            # %required data range
            # % to be implemented: ValueAfter return the date as well
            startValue = self.AdjVWAP.ValueAfter(startDate)
            endValue = self.AdjVWAP.ValueAfter(endDate)
            return 100.0 * (endValue / startValue - 1.0)

        # % return its WIND industry code as of date
        # % level could be 1,2,3,4, representing the four levels
        # % level 1 is sector
        # % level 4 is the full industry code
        def WindIndustryCode(self, date, level=None):
            date = checkDate(date)
            windID = self.WindID
            if windID in SectorIndustry.WINDIndustry:
                ts = SectorIndustry.WINDIndustry[windID]
                windIndustryCode = ts.ValueAsOf(date)
                if level and level <= 3:
                    windIndustryCode = windIndustryCode[1:(2 + 2 * level)]
            else:
                windIndustryCode = []

        # % return its WIND sector code as of date
        # % the sector code is the four digits of the full industry code
        def WindSectorCode(self, date):
            date = checkDate(date)
            windIndustryCode = self.WindIndustryCode(date)
            windSectorCode = windIndustryCode[1:4]
            return windSectorCode

        # % this is the only way to initiate a stock, which is a time
        # % consuming operation, so we just do once for each stock
        @staticmethod
        def ByWindID(windID):
            global STOCKMASTERMAP
            if windID in STOCKMASTERMAP:
                stock = STOCKMASTERMAP[windID]
            else:
                # % initiate stock properties from database
                sqlStr1 = 'select S_INFO_CODE ''Ticker'', S_INFO_NAME ''ShortName'', S_INFO_COMPNAME ''Name'''', S_INFO_EXCHMARKET ''Exchange'', S_INFO_LISTBOARD ''ListBoard'', S_INFO_LISTDATE ''ListDate''''from WINDDB.DBO.ASHAREDESCRIPTION''where S_INFO_WINDCODE=%s'
                curs = GlobalConstant.DBCONN_WIND.cursor()
                curs.execute(sqlStr1 % windID)
                row = curs.fetchone()
                stock = Stock(windID, row[1], row[2], row[3], row[4], row[5], row[6])
                curs.close()
                STOCKMASTERMAP[windID] = stock
