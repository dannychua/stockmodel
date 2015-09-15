%% header
% a static class generate pre-defined portfolio providers
% date: 7/3/2015

%%
classdef PortfolioProviders   
    methods (Static)
        % since 4/1/2009, the table AIndexHS300FreeWeight has constituents
        % and their weights on a daily basis
        % before that, the table AIndexMembers has constituents' in-and-out
        % dates, and the index can still be constructed using market cap
        
        % to validate: 
        % 1. the boundary of in-and-out dates, i.e., whether the "out" date
        % is the first day of being out or the last date of being in.
        % 2. is it constructed by total market cap or floating market cap?
        
        % A50 (上证50), which S_INFO_WINDCODE = '000016.SH'
        function a50PP = GetA50()
            % better put field name and refer to name instead of index 
            sqlString = [...
                           'select S_CON_WINDCODE stockID, TRADE_DT dt, I_WEIGHT wt' char(10)...   
                           'from WINDDB.DBO.AINDEXHS300FREEWEIGHT' char(10)...
                           'where S_INFO_WINDCODE = ''000016.SH'' and TRADE_DT>''', GlobalConstant.TestStartDate, '''' char(10)...
                           'order by TRADE_DT'
                           ];                   
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);    
            
            [~,dtIdx] = unique(curs.Data(:,2)); % extract the dates
            dates = datenum(char(curs.Data(dtIdx,2)),'yyyymmdd');
            datesLen = length(dates);
            portfolio_ts = QTimeSeries();  % initiate an array of portfolios
            for i = 1:datesLen
                dt = dates(i);
                dtIdxEnd = 0; % the last index of members on that day
                if i==datesLen
                    dtIdxEnd = size(curs.Data,1);
                else
                    dtIdxEnd = dtIdx(i+1)-1;
                end
                holdingsData = curs.Data(dtIdx(i):dtIdxEnd,[1,3]); % [ticker, weights]
                numHoldings = size(holdingsData,1);
                extraColumns = zeros(numHoldings,2);
                % add the extra columns for Shares and MarketValue
                holdingsData = [holdingsData,num2cell(extraColumns)]; 
                holdings = cell2struct(holdingsData, GlobalConstant.Holding,2);
                portfolio = Portfolio(dt, holdings);
                Add(portfolio_ts, dt, portfolio);
            end
            clear curs;
            
            closingPx = PortfolioProviders.GetIndexClosingPx('000016.SH');            
            a50PP = PortfolioProvider('A50Index', portfolio_ts, 'A50 index', closingPx);
        end

        % 中证500, which S_INFO_WINDCODE = '000905.SH'
        function zhongzheng500PP = GetZhongZheng500()
            % better put field name and refer to name instead of index 
            sqlString = [...
                           'select S_CON_WINDCODE stockID, TRADE_DT dt, I_WEIGHT wt' char(10)...   
                           'from WINDDB.DBO.AINDEXHS300FREEWEIGHT' char(10)...
                           'where S_INFO_WINDCODE = ''000905.SH'' and TRADE_DT>''', GlobalConstant.TestStartDate, '''' char(10)...
                           'order by TRADE_DT'
                           ];                   
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);    
            
            [~,dtIdx] = unique(curs.Data(:,2)); % extract the dates
            dates = datenum(char(curs.Data(dtIdx,2)),'yyyymmdd');
            datesLen = length(dates);
            portfolio_ts = QTimeSeries();  % initiate an array of portfolios
            for i = 1:datesLen
                dt = dates(i);
                dtIdxEnd = 0; % the last index of members on that day
                if i==datesLen
                    dtIdxEnd = size(curs.Data,1);
                else
                    dtIdxEnd = dtIdx(i+1)-1;
                end
                holdingsData = curs.Data(dtIdx(i):dtIdxEnd,[1,3]); % [ticker, weights]
                numHoldings = size(holdingsData,1);
                extraColumns = zeros(numHoldings,2);
                % add the extra columns for Shares and MarketValue
                holdingsData = [holdingsData,num2cell(extraColumns)]; 
                holdings = cell2struct(holdingsData, GlobalConstant.Holding,2);
                portfolio = Portfolio(dt, holdings);
                Add(portfolio_ts, dt, portfolio);
            end
            clear curs;
            
            closingPx = PortfolioProviders.GetIndexClosingPx('000905.SH');
            zhongzheng500PP = PortfolioProvider('Zhongzheng500', portfolio_ts, 'Zhongzheng500  index', closingPx);
        end
        
        % 中证800, which S_INFO_WINDCODE = '000906.SH'
        function zhongzheng800PP = GetZhongZheng800()
            % better put field name and refer to name instead of index 
            sqlString = [...
                           'select S_CON_WINDCODE stockID, TRADE_DT dt, I_WEIGHT wt' char(10)...   
                           'from WINDDB.DBO.AINDEXHS300FREEWEIGHT' char(10)...
                           'where S_INFO_WINDCODE = ''000906.SH'' and TRADE_DT>''', GlobalConstant.TestStartDate, '''' char(10)...
                           'order by TRADE_DT'
                           ];                   
            
            set(GlobalConstant.DBCONN_WIND, 'AutoCommit', 'off');
            h = GlobalConstant.DBCONN_WIND.Handle;
            stmt = h.createStatement();
            stmt.setFetchSize(1000);
            rs = stmt.executeQuery(java.lang.String(sqlString));
            [colnames, outData, totalRows] = PortfolioProviders.fetchInBatches(GlobalConstant.DBCONN_WIND, rs, 1000, 1000*1000);
            outData = outData(1:totalRows,:);
            [~,dtIdx] = unique(outData(:,2)); % extract the dates
            dates = datenum(char(outData(dtIdx,2)),'yyyymmdd');
            
            datesLen = length(dates);
            portfolio_ts = QTimeSeries();  % initiate an array of portfolios
            for i = 1:datesLen
                dt = dates(i);
                dtIdxEnd = 0; % the last index of members on that day
                if i==datesLen
                    dtIdxEnd = size(outData,1);
                else
                    dtIdxEnd = dtIdx(i+1)-1;
                end
                holdingsData = outData(dtIdx(i):dtIdxEnd,[1,3]); % [ticker, weights]
                numHoldings = size(holdingsData,1);
                extraColumns = zeros(numHoldings,2);
                % add the extra columns for Shares and MarketValue
                holdingsData = [holdingsData,num2cell(extraColumns)]; 
                holdings = cell2struct(holdingsData, GlobalConstant.Holding,2);
                portfolio = Portfolio(dt, holdings);
                Add(portfolio_ts, dt, portfolio);
            end
            clear curs;
            
            closingPx = PortfolioProviders.GetIndexClosingPx('000906.SH');
            zhongzheng800PP = PortfolioProvider('Zhongzheng800', portfolio_ts, 'Zhongzheng800  index', closingPx);
        end        
        
        % to do: HS300, ??500, CalibrationUniv, ScoringUniv
        % the way to construct HS300, ??500 is similar to A50
        % both CalibrationUniv and ScoringUniv are equal weighted
        % CalibrationUniv is all about filtering out small/illiquid stocks
        
        function closingPx = GetIndexClosingPx(idxWindID)
            sqlString = [...
                           'select TRADE_DT, S_DQ_CLOSE' char(10)...   
                           'from WINDDB.DBO.AIndexEODPrices' char(10)...
                           'where S_INFO_WINDCODE = ''', idxWindID, ''' and TRADE_DT>''', GlobalConstant.TestStartDate, '''' char(10)...                           
                           'order by TRADE_DT'
                           ];                   
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);    
            dates = datenum(char(curs.Data(:,1)),'yyyymmdd');
            % value is cell   
            closingPx = QTimeSeries(dates, curs.Data(:,2));
            clear curs;
        end
        
        
        % when the number of rows is too many, fetch the data in batches
        function [colnames, out, totalRows] = fetchInBatches(conn, rs, batchCount, maxrows)
            %FETCHINBATCHES function to fetch data in a resultset in batches.
            % [colnames, out] = fetchInBatches(conn, rs, batchCount, maxrows)
            % conn : Database Connection Object
            % rs : ResultSet object 
            % batchCount: integer indicating number of rows to be fetched in each batch
            % maxrows: Total number of rows expected. This number will be used in
            % initialization of the output cell array and thus improve performance.

            rsmd = getMetaData(rs);
            ncols = getColumnCount(rsmd);
            nrows = batchCount;
            iter = 0;

            %Initialize for better performance
            colnames = cell(ncols, 1);
            out = cell(maxrows, ncols);
            totalRows = 0;
            
            while(nrows > 0)

                %to fetch the data
                
                h = conn.Handle;

                if(batchCount ~= 0)
                    fet = com.mathworks.toolbox.database.fetchTheData(h, rs, '', batchCount);
                else
                    fet = com.mathworks.toolbox.database.fetchTheData(h, rs, '');
                end

                md = getTheMetaData(fet);
                status = validResultSet(fet,md);

                if(status ~=0 )

                    %Get preferences
                    p = setdbprefs({'NullStringRead';'NullNumberRead';'DataReturnFormat'});
                    tmpNullNumberRead = 'NullNumberReadPlaceHolderCFG3358';

                    %Fetch batchCount rows
                    resultSetMetaData = getValidResultSet(fet,md);
                    dataFetched = dataFetch(fet,resultSetMetaData,p.NullStringRead,tmpNullNumberRead);

                    if(size(dataFetched) == 0)
                        break;
                    end

                    %Convert java.util.vector to cell array
                    %Check if num row is less than batchCount
                    nrows =  size(dataFetched) / ncols;
                    totalRows = totalRows + nrows;  % added by FX
                    if (nrows == 0)
                        break;
                    end

                    %if (nrows > 0 && nrows < batchCount)
                    if (nrows < batchCount)
                        data = system_dependent(44,dataFetched,nrows)';
                    else
                        data = system_dependent(44,dataFetched,batchCount)';
                    end

                    %Convert NullNumberRead value into numeric value
                    i = find(strcmp(data,tmpNullNumberRead));
                    data(i) = {str2num(p.NullNumberRead)};

                    out(iter*batchCount+1:iter*batchCount+nrows, :) = data;
                    iter = iter + 1;
                else
                    error('No valid resultset');
                end
            end

            %get columnnames
            for i=1:ncols
                colnames{i} =  char(getColumnName(rsmd, i));
            end
            %close resultset
            rs.close;
        end
    end

end
