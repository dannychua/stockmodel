%% header
% handle a timeseries of portfolios and the related logic
% date: 7/3/2015

%%
% it is a handle class
classdef PortfolioProvider < handle
    properties
        Name                % the ID of the portfolio provider
        Description         % the description of the portfolio provider
        AvailableDates      % the dates on which a portfolio exist
        Portfolios          % the timeseries of portfolios
        ClosingPx           % closing price time series, optional, only available for indices
        Desc                % description of the portfolio provider
    end
    
    methods
        % portfolio_ts is a time series of portfolio
        function obj = PortfolioProvider(name, portfolios, desc, closingPx)
            obj.Name = name;
            obj.Portfolios = portfolios;
            obj.AvailableDates = portfolios.Dates;            
            if(nargin>2)
                Desc = desc;
                if(nargin > 3)
                    obj.ClosingPx = closingPx;
                end
            end
        end
        
        % return the portfolio on date if it exists
        % otherwise return empty 
        function portfolio = GetPortfolioOn(obj, date)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            portfolio = ValueOn(obj.Portfolios, date);
        end

        % return the portfolio on dt if it exists
        % if it doesn't exist, then take the most recent portfolio and don't adjust its weights
        % if reWeightTo100 is true, re-scale the long side of the portfolio to be 100%
        % if no portfolio exists before dt, return empty
        function portfolio = GetPortfolioAsofFixed(obj, date, reWeightTo100)            
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            if(nargin <3) 
                reWeightTo100 = 0;
            end
            
            portfolio = ValueAsOf(obj.Portfolios, date); 
            if nargin>2 && reWeightTo100
                ReWeightTo100(portfolio);
            end            
        end
        
        % return the portfolio on dt if it exists
        % if it doesn't exist, then take the most recent portfolio and carry-over its holdings to date
        % weights are adjusted to reflect the stock returns from the AsOfDate to date
        % if reWeightTo100 is true, re-scale the long side of the portfolio to be 100%
        % if no portfolio exists before dt, return empty
        function portfolio = GetPortfolioAsof(obj, date, reWeightTo100)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            if(nargin <3) 
                reWeightTo100 = 0;
            end
            
            portfolio = ValueAsOf(obj.Portfolios, date); 
            HeldToDate(portfolio, date, false);
            
            if nargin>2 && reWeightTo100
                ReWeightTo100(portfolio);
            end            
        end
        
        function ppRet = TotalReturnInRange(obj, startDate, endDate)
            if (isemptry(obj.ClosingPx))
                ppRet = nan;  % to be implemented
            else
                startValue = ValueAsOf(obj.ClosingPx, startDate);
                endValue = ValueAsOf(obj.ClosingPx, endDate);
                ppRet = 100.0*(endValue/startValue - 1.0);
            end
        end

        function ppRet = TotalReturnInRange_Bk(obj, startDate, endDate)
            if (isempty(obj.ClosingPx))
                ppRet = nan;  % to be implemented
            else
                startValue = ValueAfter(obj.ClosingPx, startDate);
                endValue = ValueAfter(obj.ClosingPx, endDate);                
                ppRet = 100.0*(endValue/startValue - 1.0);
            end
        end
        
        function dates = get.AvailableDates(obj)
            dates = obj.AvailableDates;
        end
        
        function closingPx = get.ClosingPx(obj)
            closingPx = obj.ClosingPx;
        end

                
    end
    
end
