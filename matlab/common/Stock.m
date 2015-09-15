%% header
% this class is to represent a stock
% Date: 7/3/2015 created
%       8/1/2015 implemented many properties & methods

%%
% it is a handle class
classdef Stock < handle
    properties (GetAccess = private)
        
    end
    
    properties
        WindID          % Wind stock ID, unique
        Ticker          % ticker used on exchanges 
        ShortName       % the short name of the company
        Name            % the name of the company
        Exchange        % exchange
        ListBoard       % the list board
        ListDate        % the list date
       
        
        AdjClosingPx    % adjusted closing prices
        AdjVWAP         % adjusted VWAP
        ClosingPx       % closing prices
        VolumeShares    % trading volume in shares
        VolumeValue     % trading volume in thousands of RMB 
        FloatingShares  % floating shares
        
        % ======= to be implemented in the future
        TradingStatus   % trading status: trading(in Chinese), no trading(in Chinese), XR, XD, N, DR, NULL
        % sector/industry/daily prices etc ... to be implemented later
        %DelistDate
        %Currency  
        % ...
        
        
    end
    
    methods (Access = private)
        % private because we want to keep only one instance of each Stock
        function obj = Stock(windID, ticker, shortName, name, exchange, listBoard, listDate)
            obj.WindID = windID;
            obj.Ticker = ticker;
            obj.ShortName = shortName;
            obj.Name = name;
            obj.Exchange = exchange;
            obj.ListBoard = listBoard;
            obj.ListDate = listDate;
        end
        
        function getDatafromDB(obj)
            sqlString = ['select TRADE_DT, S_DQ_CLOSE, S_DQ_VOLUME, S_DQ_AMOUNT*1000, S_DQ_ADJCLOSE, S_DQ_AVGPRICE*S_DQ_ADJFACTOR adjVWAP' char(10)... 
                'from WindDB.dbo.ASHAREEODPRICES where S_INFO_WINDCODE = ''', obj.WindID, ''' and S_DQ_TRADESTATUS != ''Í£ÅÆ''and TRADE_DT>''', GlobalConstant.TestStartDate, ''' order by trade_dt'];
%             sqlString = ['select TRADE_DT, S_DQ_CLOSE, S_DQ_VOLUME, S_DQ_AMOUNT*1000, S_DQ_ADJCLOSE, S_DQ_AVGPRICE*S_DQ_ADJFACTOR adjVWAP' char(10)... 
%                 'from WindDB.dbo.ASHAREEODPRICES where S_INFO_WINDCODE = ''', obj.WindID, ''' order by trade_dt'];
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);
            dates = datenum(char(curs.Data(:,1)),'yyyymmdd');
            % value is cell   
            obj.ClosingPx = QTimeSeries(dates, curs.Data(:,2));
            obj.VolumeShares = QTimeSeries(dates, curs.Data(:,3)); 
            obj.VolumeValue = QTimeSeries(dates, curs.Data(:,4)); 
            obj.AdjClosingPx = QTimeSeries(dates, curs.Data(:,5)); 
            obj.AdjVWAP = QTimeSeries(dates, curs.Data(:,6));    
            clear curs;
        end
    end
    
    methods
        function id = get.WindID(obj)
            id = obj.WindID;
        end

        function ClosingPx = get.ClosingPx(obj)
            if isempty(obj.ClosingPx)
                getDatafromDB(obj);
            end
            ClosingPx = obj.ClosingPx;
        end        
        
        function VolumeShares = get.VolumeShares(obj)
            if isempty(obj.VolumeShares)
                getDatafromDB(obj);
            end
            VolumeShares = obj.VolumeShares;
        end        
        
        function VolumeValue = get.VolumeValue(obj)
            if isempty(obj.VolumeValue)
                getDatafromDB(obj)
            end
            VolumeValue = obj.VolumeValue;
        end        
        
        function AdjClosingPx = get.AdjClosingPx(obj)
            if isempty(obj.AdjClosingPx)
                getDatafromDB(obj)
            end
            AdjClosingPx = obj.AdjClosingPx;
        end
                
        function AdjVWAP = get.AdjVWAP(obj)
            if isempty(obj.AdjVWAP)
                getDatafromDB(obj)
            end
            AdjVWAP = obj.AdjVWAP;
        end

        function FloatingShares = get.FloatingShares(obj)
            if isempty(obj.FloatingShares)                
                sqlString = ['select TRADE_DT, FLOAT_A_SHR_TODAY*10000 from WindDB.dbo.ASHAREEODDERIVATIVEINDICATOR  where S_INFO_WINDCODE = ''', obj.WindID, ''' and TRADE_DT>''', GlobalConstant.TestStartDate, ''' order by trade_dt'];
                curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
                curs = fetch(curs);
                dates = datenum(char(curs.Data(:,1)),'yyyymmdd');
                obj.FloatingShares = QTimeSeries(dates, curs.Data(:,2)); % value is cell               
            end
            FloatingShares = obj.FloatingShares;
        end        

        function price = PriceOnDate(obj, date)
            price = ValueOn(obj.ClosingPx, date);
            if isempty(price)
                price = NaN;
            end
        end
        
        function mktCap = FloatMarketCap(obj, date)
            mktCap = ValueAsOf(obj.ClosingPx, date) * ValueAsOf(obj.FloatingShares, date);
            if isempty(mktCap)
                mktCap = NaN;
            end
        end
        
        % calculate total returns from startDate to endDate using Adjusted closing prices with asof semantics 
        % if startDate < FirstTradingDate, return NaN
        % if endDate > LastTradingDate (delisted stock) or today, replace
        % endDate as of the most recent date in the price series
        % stkReturn is in percentage
        function stkReturn = TotalReturnInRange(obj, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            firstDt = FirstDate(obj.AdjClosingPx);
            if (startDate < firstDt) 
                stkReturn = NaN;
                return;
            end
            
            startValue = ValueAsOf(obj.AdjClosingPx, startDate);
            endValue = ValueAsOf(obj.AdjClosingPx, endDate);
            stkReturn = 100.0*(endValue/startValue - 1.0);
        end
        
        % calculate total returns from startDate to endDate using Adjusted VWAP with asof semantics 
        % if startDate < FirstTradingDate, return NaN
        % if endDate > LastTradingDate (delisted stock) or today, replace
        % endDate as of the most recent date in the price series
        % stkReturn is in percentage
        function stkReturn = TotalReturnInRange_VWAP(obj, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            firstDt = FirstDate(obj.AdjVWAP);
            if (startDate < firstDt) 
                stkReturn = NaN;
                return;
            end
            
            startValue = ValueAsOf(obj.AdjVWAP, startDate);
            endValue = ValueAsOf(obj.AdjVAWP, endDate);
            stkReturn = 100.0*(endValue/startValue - 1.0);
        end

        % to be implemented: handle limit up/down days: e.g. if to buy a
        % stock which is limited up on the following day, wait for a day
        % when there is no limited up; vice versa for selling stocks.
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
        function stkReturn = TotalReturnInRange_Bk(obj, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            firstDt = FirstDate(obj.AdjClosingPx);
            if (startDate < firstDt) 
                stkReturn = NaN;
                return;
            end
            
            %better return the return and the date range, so that the
            %caller knows how far off the return date range is from the
            %required data range
            % to be implemented: ValueAfter return the date as well
            startValue = ValueAfter(obj.AdjVWAP, startDate);
            endValue = ValueAfter(obj.AdjVWAP, endDate);
            stkReturn = 100.0*(endValue/startValue - 1.0);
        end
        
        % return its WIND industry code as of date
        % level could be 1,2,3,4, representing the four levels
        % level 1 is sector
        % level 4 is the full industry code
        function windIndustryCode = WindIndustryCode(obj, date, level)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            windID = obj.WindID;
            if (isKey(SectorIndustry.WINDIndustry, windID))
                ts = SectorIndustry.WINDIndustry(windID);
                windIndustryCode = ValueAsOf(ts, date);                 
                if(nargin > 2 && level <=3)
                    windIndustryCode = windIndustryCode(1:(2+2*level));
                end
            else
                windIndustryCode = [];
            end
        end
        
        % return its WIND sector code as of date
        % the sector code is the four digits of the full industry code
        function windSectorCode = WindSectorCode(obj, date)
            windIndustryCode = WindIndustryCode(obj, date);
            windSectorCode = windIndustryCode(1:4);
        end
        
        
    end
    
    methods (Static)        
        % this is the only way to initiate a stock, which is a time
        % consuming operation, so we just do once for each stock
        function stock = ByWindID(windID)            
            global STOCKMASTERMAP;
            if STOCKMASTERMAP.isKey(windID)
                stock = STOCKMASTERMAP(windID);
            else
                % initiate stock properties from database                
                sqlStr1 = [...
                    'select S_INFO_CODE ''Ticker'', S_INFO_NAME ''ShortName'', S_INFO_COMPNAME ''Name''' ...
                    ', S_INFO_EXCHMARKET ''Exchange'', S_INFO_LISTBOARD ''ListBoard'', S_INFO_LISTDATE ''ListDate'''   char(10)...                    
                    'from WINDDB.DBO.ASHAREDESCRIPTION' char(10)...
                    'where S_INFO_WINDCODE=''', windID, '''' char(10)...
                    ];
                curs = exec(GlobalConstant.DBCONN_WIND, sqlStr1);
                curs = fetch(curs);    
                % it might be error-prone using index instead of name
                stock = Stock(windID, curs.Data{1}, curs.Data{2}, curs.Data{3}, curs.Data{4}, curs.Data{5}, curs.Data{6} );
                clear curs; 
                STOCKMASTERMAP = [STOCKMASTERMAP; containers.Map(windID,stock)];
            end
        end
    end
end