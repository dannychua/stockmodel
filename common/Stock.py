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
            curs.execute(sqlString % (self.WindID, GlobalConstant.TestStartDate.strftime('%Y%m%d'))) #convert to string first
        rows = curs.fetchall()
        curs.close()
        df = pd.DataFrame(rows)
        self.FloatingShares = QTimeSeries(df.TRADE_DT.tolist(), df.FloatingShares.tolist()) #% value is cell
        return self.FloatingShares

        function price = PriceOnDate(self, date)
            price = ValueOn(self.ClosingPx, date)
            if isempty(price)
                price = NaN
            end
        end

        function mktCap = FloatMarketCap(self, date)
            mktCap = ValueAsOf(self.ClosingPx, date) * ValueAsOf(self.FloatingShares, date)
            if isempty(mktCap)
                mktCap = NaN
            end
        end

        % calculate total returns from startDate to endDate using Adjusted closing prices with asof semantics
        % if startDate < FirstTradingDate, return NaN
        % if endDate > LastTradingDate (delisted stock) or today, replace
        % endDate as of the most recent date in the price series
        % stkReturn is in percentage
        function stkReturn = TotalReturnInRange(self, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd')
            end

            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd')
            end

            firstDt = FirstDate(self.AdjClosingPx)
            if (startDate < firstDt)
                stkReturn = NaN
                return
            end

            startValue = ValueAsOf(self.AdjClosingPx, startDate)
            endValue = ValueAsOf(self.AdjClosingPx, endDate)
            stkReturn = 100.0*(endValue/startValue - 1.0)
        end

        % calculate total returns from startDate to endDate using Adjusted VWAP with asof semantics
        % if startDate < FirstTradingDate, return NaN
        % if endDate > LastTradingDate (delisted stock) or today, replace
        % endDate as of the most recent date in the price series
        % stkReturn is in percentage
        function stkReturn = TotalReturnInRange_VWAP(self, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd')
            end

            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd')
            end

            firstDt = FirstDate(self.AdjVWAP)
            if (startDate < firstDt)
                stkReturn = NaN
                return
            end

            startValue = ValueAsOf(self.AdjVWAP, startDate)
            endValue = ValueAsOf(self.AdjVAWP, endDate)
            stkReturn = 100.0*(endValue/startValue - 1.0)
        end

        % to be implemented: handle limit up/down days: e.g. if to buy a
        % stock which is limited up on the following day, wait for a day
        % when there is no limited up vice versa for selling stocks.
        %
        % shall be used in backtest
        % assume the investment decision is made on startDate
        % to be conservative:
        % the entry price is the VWAP on the trading day following startDate
        % the exit price is the VWAP on the trading day following endDate
        % note that if stock stop-trading days should be removed
        %
        % if startDate < FirstTradingDate, return NaN
        % if endDate > LastTradingDate (delisted stock) or today, replace
        % endDate as of the most recent date in the price series
        % stkReturn is in percentage
        function stkReturn = TotalReturnInRange_Bk(self, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd')
            end

            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd')
            end

            firstDt = FirstDate(self.AdjClosingPx)
            if (startDate < firstDt)
                stkReturn = NaN
                return
            end

            %better return the return and the date range, so that the
            %caller knows how far off the return date range is from the
            %required data range
            % to be implemented: ValueAfter return the date as well
            startValue = ValueAfter(self.AdjVWAP, startDate)
            endValue = ValueAfter(self.AdjVWAP, endDate)
            stkReturn = 100.0*(endValue/startValue - 1.0)
        end

        % return its WIND industry code as of date
        % level could be 1,2,3,4, representing the four levels
        % level 1 is sector
        % level 4 is the full industry code
        function windIndustryCode = WindIndustryCode(self, date, level)
            if ischar(date)
                date = datenum(date, 'yyyymmdd')
            end

            windID = self.WindID
            if (isKey(SectorIndustry.WINDIndustry, windID))
                ts = SectorIndustry.WINDIndustry(windID)
                windIndustryCode = ValueAsOf(ts, date)
                if(nargin > 2 && level <=3)
                    windIndustryCode = windIndustryCode(1:(2+2*level))
                end
            else
                windIndustryCode = []
            end
        end

        % return its WIND sector code as of date
        % the sector code is the four digits of the full industry code
        function windSectorCode = WindSectorCode(self, date)
            windIndustryCode = WindIndustryCode(self, date)
            windSectorCode = windIndustryCode(1:4)
        end


    end

    methods (Static)
        % this is the only way to initiate a stock, which is a time
        % consuming operation, so we just do once for each stock
        function stock = ByWindID(windID)
            global STOCKMASTERMAP
            if STOCKMASTERMAP.isKey(windID)
                stock = STOCKMASTERMAP(windID)
            else
                % initiate stock properties from database
                sqlStr1 = [...
                    'select S_INFO_CODE ''Ticker'', S_INFO_NAME ''ShortName'', S_INFO_COMPNAME ''Name'''...
        ', S_INFO_EXCHMARKET ''Exchange'', S_INFO_LISTBOARD ''ListBoard'', S_INFO_LISTDATE ''ListDate'''
        char(10)...
        'from WINDDB.DBO.ASHAREDESCRIPTION'
        char(10)...
        'where S_INFO_WINDCODE=''', windID, '''' char(10)...
                    ]
                curs = exec(GlobalConstant.DBCONN_WIND, sqlStr1)
                curs = fetch(curs)
                % it might be error-prone using index instead of name
                stock = Stock(windID, curs.Data{1}, curs.Data{2}, curs.Data{3}, curs.Data{4}, curs.Data{5}, curs.Data{6} )
                clear curs
                STOCKMASTERMAP = [STOCKMASTERMAP containers.Map(windID,stock)]
            end
        end
    end
end
