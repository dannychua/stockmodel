%% header
% handle statistics of a return series which is a time series

% date: 8/2/2015

%%

% 
classdef ReturnSeries < QTimeSeries
    properties
        AnnMean         % annualized mean
        AnnStd          % annualized stdev
        SR              % Sharpe ratio = annualized mean/stdev
        Returns         % periodic returns
        CompCumReturns  % compound cumulative returns, starting from 1.0
        CumReturns      % non-compound cumulative returns, starting from 1.0
        
        % to be implemented
        TStat           % SR*sqrt(number of years)
        HitRate         % number of periods with positive returns / number of periods
        MaxDrawdown     % maximum drawdown
        SortinoRatio    % annualized mean / std(negative returns)        
    end

    properties (Access = private)
        annScalar       % a scalar used to annualize periodic returns
    end
    
    methods (Access = private)
        function calc(obj)
            if length(obj.Dates)>2
                diff = obj.Dates(2) - obj.Dates(1);
                if diff == 1 || diff == 3
                    annScalar = 252; % weekday
                elseif diff == 7
                    annScalar = 52;  % weekly 
                elseif diff >25 && diff<33
                    annScalar = 12;  % monthly
                elseif  diff >85 && diff<95
                    annScalar = 4;   % quarterly
                end
            end
                        
            vals = cell2mat(obj.Values);
            obj.Returns = vals;
            avg = nanmean(vals);  %% need to handle the number of periods in a year, to be implemented
            obj.AnnMean = avg * annScalar;
            stdev = nanstd(vals);
            obj.AnnStd = stdev * sqrt(annScalar);
            obj.SR = sqrt(annScalar)*avg/stdev;
            
            % need to handle the number of periods in a year, to be implemented
            
            numPeriods = length(vals);
            obj.CompCumReturns = zeros(numPeriods,1);
            obj.CumReturns = zeros(numPeriods,1);
            obj.CompCumReturns(1) = 1+vals(1)*0.01;
            obj.CumReturns(1) = vals(1);
            for i=2:numPeriods
                obj.CompCumReturns(i) = obj.CompCumReturns(i-1)*(1+vals(i)*0.01);
                obj.CumReturns(i) = obj.CumReturns(i-1)+vals(i);                
            end
        end
    end
    
    methods
        function obj = ReturnSeries(dates, values)
%             if (nargin == 0)
                obj@QTimeSeries();  
%             else
%                 obj@QTimeSeries(dates, values);            
            annScalar  = 12.0; % assuming time series is monthly
        end
           
        function plot(obj, type, desc)
            y = [];
            myTitle='';
            if(nargin>2)
                myTitle = desc;
            end
            
            if (nargin <2 || strcmp(type,'cr'))
                plot(obj.Dates, obj.CumReturns);
                title([myTitle, 'Cumulative Returns']);
                y = [5,0,-5];
            elseif(strcmp(type,'ccr'))
                plot(obj.Dates, obj.CompCumReturns);
                title([myTitle, 'Compounding Cumulative Returns']);
                y = [1.05, 1, 0.95];
            else 
                plot(obj.Dates, obj.Returns);
                title([myTitle, 'Returns']);
                y = [5,0,-5];
            end
            datetick('x','mm/yy');
            
            % x and y better be dynamic, to be implemented
            x = obj.Dates(length(obj.Dates)-20);
            text(x, y(1), ['AnnMean ',num2str(obj.AnnMean,'%5.2f')]);
            text(x, y(2), ['AnnStd  ',num2str(obj.AnnStd,'%5.2f')]);
            text(x, y(3), ['SR     ',num2str(obj.SR,'%5.2f')]);
        end
        
        function annmean = get.AnnMean(obj)
            if( isempty(obj.AnnMean))
                calc(obj)
            end
            annmean = obj.AnnMean;
        end
        
        function annstd = get.AnnStd(obj)
            if( isempty(obj.AnnStd))
                calc(obj)
            end
            annstd = obj.AnnStd;
        end
        
        function sr = get.SR(obj)
            if( isempty(obj.SR))
                calc(obj)
            end
            sr = obj.SR;
        end

        function rets = get.Returns(obj)
            if( isempty(obj.Returns))
                calc(obj)
            end
            rets = obj.Returns;
        end
        
        function cumRets = get.CompCumReturns(obj)
            if( isempty(obj.CompCumReturns))
                calc(obj)
            end
            cumRets = obj.CompCumReturns;
        end

        function cumRets = get.CumReturns(obj)
            if( isempty(obj.CumReturns))
                calc(obj)
            end
            cumRets = obj.CumReturns;
        end
        
        
    end
    
end
