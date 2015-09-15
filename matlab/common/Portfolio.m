%% header
% handle a portfolio and the related logic
% a portfolio is a set of holdings with a date when the portfolio is
% evaluated
% date: 7/3/2015

%%
% it is a handle class
classdef Portfolio < handle
    properties
        Date            % the date on which the portfolio is evaluated
        Holdings        % the stocks held and their weights in the portfolio, could be empty
        MarketValue     % the market value of the portfolio, could be negative or null
    end
    
    methods
        % holdings could be empty
        % dim is the length of the portfolio array, used to initiate an array of portfolios
        % to be implemented: it'd better remove 'dim' as a parameter
        function obj = Portfolio(date, holdings)
            obj.Date = date;
            if(nargin>1) 
                obj.Holdings = holdings;
            end
        end
        
        function AddHolding(obj, holding)
            obj.Holdings = [obj.Holdings; holding];
        end
        
        % re-weight the portfolio to be equal weighted
        function ReWeightEqual(obj)            
            if ~isempty(obj.Holdings)    % if the portfolio has holdings
                len = length(obj.Holdings);
                wt = 100.0/len;
                for i = 1:len
                    obj.Holdings(i).Weight = wt;
                end
            end
        end

        % re-weight the long side to be 100%
        function ReWeightTo100(obj)            
            if ~isempty(obj.Holdings)    % if the portfolio has holdings
                wts = [obj.Holdings.Weight];
                total = sum(wts(wts>0));   % sum the positive weights only
                scalar = 100.0/total;
                len = length(obj.Holdings);
                for i = 1:len
                    obj.Holdings(i).Weight = obj.Holdings(i).Weight*scalar;
                end
            end
        end
                
        % market cap is evaluated as of 'date'
        function portfolio = ReWeightMarketCap(obj)            
            if ~isempty(obj.Holdings)    % if the portfolio has holdings
                len = length(obj.Holdings);
                mktCaps = zeros(1,len); % note that Weights is 1 X n
                total = 0;
                for i = 1:len
                    stk = Stock.ByWindID(obj.Holdings(i).StockID);
                    mktCaps(i) = FloatMarketCap(stk, obj.Date);
                    if isnan(mktCaps(i))
                        mktCaps(i) = 0;
                    end
                    total = total + mktCaps(i);
                end
                for i = 1:len
                    obj.Holdings(i).Weight = 100.0*mktCaps(i)/total;
                end
            end
        end
        
        % hold the portfolio obj through "date"
        % if reweightTo100 = true, the total long weight is 100%
        % otherwise (default), don't reweight it
        function HeldToDate(obj, date, reweightTo100)
            if(obj.Data < daet && ~isempty(obj.Holdings))
                len = length(obj.Holdings);
                for i = 1:len
                    stk = Stock.ByWindID(obj.Holdings(i).StockID);
                    ret = TotalReturnInRange(stk, obj.Date, date);
                    if isnan(ret)
                        ret = 0;
                    end
                    obj.Holdings(i).Weight = obj.Holdings(i).Weight*(1+0.01*ret);
                end
                if(nargin > 2 && reweightTo100)
                    ReWeightTo100(obj);
                end
            end
        end
        
        % calculate total returns of the portfolio from startDate to endDate
        % pfReturn is in percentage
        function pfReturn = TotalReturnInRange(obj, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end

            pfReturn = 0;
            validWt = 0;
            numHoldings = length(obj.Holdings);
            for i = 1:numHoldings
                stk = Stock.ByWindID(obj.Holdings(i).StockID);
                stkRet = TotalReturnInRange(stk, startDate, endDate);
                if ~isnan(stkRet)
                    validWt = validWt + obj.Holdings(i).Weight;
                    pfReturn = pfReturn + stkRet * obj.Holdings(i).Weight * 0.01;
                end
            end
            if validWt < 95
                error('less than 95% of the portfolio has valid returns')
            end
        end

        function stockIDs = GetStockIDs(obj)
            stockIDs = char(obj.Holdings.StockID);
        end                
        
        function holdings = get.Holdings(obj)
            holdings = obj.Holdings;
        end        
        
    end
    
end
