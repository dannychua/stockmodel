%% header
% handle a time series and the related logic
% date: 7/10/2015

%%

% 
classdef QTimeSeries < handle  
    properties (GetAccess = private)
        valueIndex      % vector of index of Values, mapping sorted Dates to Values
    end 
    
    properties
        Dates           % dates on which values exist, always sorted up
        Values          % cell, could be any objects, not sorted, referenced by valueIndex
    end
    
    methods
        % if the type of value is unknown, how to pre-allocating space for dates and values??
        % multiple scenarios:
        % 1. pass in an array of dates and values
        % 2. generate an empty timeseries with or without pre-specified
        % size of the dates
        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function obj = QTimeSeries(dates, values)                
            if (nargin == 0)
                obj.Dates = [];   
                obj.Values = {};
                obj.valueIndex = [];
            else
                if (length(dates) ~= length(values))
                    error('dates has different length as values');
                end
                
                if ischar(dates)
                    dates = datenum(dates, 'yyyymmdd');
                end
                
                [dates,obj.valueIndex] = sortrows(dates);                                

                obj.Dates = dates;
                obj.Values = values;
            end
        end
        
        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function Add(obj, date, value)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            obj.Dates = [obj.Dates;date];
            obj.Values{length(obj.Dates)} = value;
            obj.valueIndex = [obj.valueIndex;length(obj.Dates)];
            A = [obj.Dates, obj.valueIndex]; % always sort dates along with index
            B = sortrows(A, 1);
            obj.Dates = B(:,1);
            obj.valueIndex = B(:,2);
        end
        
        % return the value on date if the date exists
        % otherwise return what ??
        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function val = ValueOn(obj,date)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            
            [x,y]=find(obj.Dates == date);
            if isempty(x)
                val = [];  % set it to empty
            else
                val=obj.Values{obj.valueIndex(x)};
            end
        end
        
        % return the value as of date         
        % if date < the first date, return NaN
        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function val = ValueAsOf(obj,date)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            rtn = find(obj.Dates <= date);  %find is not very efficient, and better change to log2(n) alg
            idx = length(rtn);
            if (idx == 0)
                val = [];
            else
                val = obj.Values{obj.valueIndex(idx)};
            end
        end
        
        % return the value immediately after date 
        % if date > the last date, return NaN        
        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function val = ValueAfter(obj,date)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            rtn = find(obj.Dates > date);  %find is not very efficient, and better change to log2(n) alg
            if (length(rtn) == 0)
                val = NaN;
            else
                val = obj.Values{obj.valueIndex(rtn(1))};
            end
        end
        
        function yesno = Contains(obj, date)
            if(isempty(obj)) 
                yesno = false;
            elseif (ismember(obj.Dates,date))
                yesno = true;
            else
                yesno = false;
            end
        end
        
        function plotTS(obj, Title)
            if (~isnumeric(obj.Values{1}))
                error('its value is not numeric, so it can not be ploted');
            else
                plot(obj.Dates, cell2mat(obj.Values));
                if (nargin>1)
                    title(Title);
                end
                datetick('x','mm/yy');
            end
        end
        

        % date is either double in the format of datenum, or char in the
        % format of 'yyyymmdd'
        function Remove(obj, date)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            % to be implemented
        end
        
        function count = length(obj)
            count = length(obj.Dates);
        end

        function dates = get.Dates(obj)
            dates = obj.Dates;
        end
        
        function firstDate = FirstDate(obj)
            firstDate = obj.Dates(1);
        end
    end
    
end
