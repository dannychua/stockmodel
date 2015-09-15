%% header
% handle a holding and the related logic
% date: 7/5/2015

%%

% QDate has the format of yyyymmdd
classdef QDate       
    methods (Static)
        % please refer to GlobalConstant.TradingDates to avoid unnecessary DB query        
        function dates = GetAllTradingDays()            
            sqlString = ['select TRADE_DAYS from WindDB.dbo.ASHARECALENDAR where s_info_exchmarket = ''SSE'' and TRADE_DAYS>''', GlobalConstant.TestStartDate, ''' order by TRADE_DAYS'];
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);
            dates = datenum(char(curs.Data),'yyyymmdd');
            
            % Shanghai exchange had different trading dates from Shenzhen
            % in the early period. To avoid issues, we set start date to be the first date after 1998-01-01
            startDate = datenum('19980101','yyyymmdd');  
            dates = dates(dates>startDate);
            clear curs;                
        end
        

        % find all trading trades between startDate and endDate
        % including startDate and endDate if they are trading days
        % startDate and endDate are either datenum or 'yyyymmdd'
        function dates = TradingDaysBtw(startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end

            dates = GlobalConstant.TradingDates(GlobalConstant.TradingDates>=startDate & GlobalConstant.TradingDates <= endDate);
        end

        % find all month beginnings between startDate and endDate
        % including startDate and endDate if they are month beginnings
        function dates = MonthBeginningBtw(startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            startDateVec = datevec(startDate);
            endDateVec = datevec(endDate);
            dates = zeros(months(startDate,endDate)+2,1); % allocate more than it needs
            i = 1;
            for y = startDateVec(1):endDateVec(1)
                for m = 1:12
                    if (y == startDateVec(1))
                        if(m >= startDateVec(2))
                            dt = datenum(y,m,1);
                            dates(i) = dt;
                            i = i+1;
                        end
                    else
                        dt = datenum(y,m,1);
                        dates(i) = dt;
                        i = i+1;
                    end
                end
            end
            dates = dates(dates>= startDate & dates<=endDate);
        end
        
        % find all month ends between startDate and endDate
        % including startDate and endDate if they are month ends
        function dates = MonthEndsBtw(startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            dates = QDate.MonthBeginningBtw(startDate, endDate);
            dates = dates-1;            
            dates = dates(dates>= startDate & dates<=endDate);
            if(eomdate(endDate) == endDate)
                dates = [dates;endDate];
            end
        end
        
        % find all week ends between startDate and endDate
        % including startDate and endDate if they are week ends
        function dates = WeekEndsBtw(startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end
            
            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end
            
            % 1997-12-27, Saturday, 729751
            % temporary solution; can only handle Sat b/w 1997-12-27 ~ 2015-07-25
            dates = 729751:7:736170;
            %c = datestr(b,'yyyymmdd ddd');  %% validation
            dates = dates(dates>=startDate & dates<=endDate);
            dates = dates';
        end
        
        % return the calendar day which is equal to dt + shift
        % shift is an integer, and can be 0, positive or negative; 
        function date = AddDays(date, shift)
            if ischar(date)
                date = datenum(date, 'yyyymmdd');
            end
            date = date+shift;
        end
        
        % return the trading day which is equal to dt + shift if dt is a trading date, 
        % otherwise equal to (dt+0) + shift, where (dt+0) is the trading day prior to “dt?
        % and shift is the number of trading days
        % shift is an integer, and can be 0, positive or negative; 
        function date = FindTradingDay(dt, shift)
            if ischar(dt)
                date = datenum(dt, 'yyyymmdd');
            end

            len = length(GlobalConstant.TradingDates);
            
            x = 0; % the index of dt in the trading-days array
            if(dt < GlobalConstant.TradingDates(1))
                x = 1;
                warning('dt is before the first trading date');
            elseif(dt > GlobalConstant.TradingDates(len))
                x = len;
                warning('dt is after the last trading date');
            else            
                % the codes find the index of dt, s.t.
                % GlobalConstant.TradingDates(idx) == dt
                % or GlobalConstant.TradingDates(idx) < dt && GlobalConstant.TradingDates(idx+1) > dt
                startIdx = 1;
                endIdx = len;
                idx = 0;                
                while(idx<=0)
                    if(dt == GlobalConstant.TradingDates(startIdx))
                        idx = startIdx;
                    elseif(dt == GlobalConstant.TradingDates(endIdx))
                        idx = endIdx;
                    else
                        mid = floor((endIdx-startIdx)/2);
                        if(mid<=0)
                            idx = startIdx;                   
                        else
                            if(dt==GlobalConstant.TradingDates(startIdx+mid))
                                idx = startIdx+mid;
                            elseif(dt<GlobalConstant.TradingDates(startIdx+mid))
                                endIdx = startIdx+mid-1;
                            else
                                startIdx = startIdx+mid+1;
                            end
                        end                    
                    end
                end
                x = idx;
            end
            
            if(nargin>1) % shift is provided
                x = x + shift;
                if(x<1)
                    x = 1;
                    warning('shift is too negative s.t. it goes before the first trading day');
                elseif (x>len)
                    x = len;
                    warning('shift is too large s.t. it goes after the last trading day');
                end
            end
            date = GlobalConstant.TradingDates(x);            
        end
        
        function dates = UnionDistinct(dates1, dates2)
            dates = [dates1;dates2];
            dates = unique(dates);
            dates = sortrows(dates);
        end
                       
        function UnitTests()
            dt1 = datenum(1990,1,1);
            dt2 = datenum(2990,1,1);
            dt3 = datenum(2015,1,1);
            dt4 = datenum(2015,1,6);
%             datestr(QDate.FindTradingDay(dt1),'yyyymmdd')
%             datestr(QDate.FindTradingDay(dt2),'yyyymmdd')
%             datestr(QDate.FindTradingDay(dt3),'yyyymmdd')
%             datestr(QDate.FindTradingDay(dt4),'yyyymmdd')
            
            dt5 = datenum(2014,6,30);
            %datestr(QDate.MonthBeginningBtw(dt5, dt3),'yyyymmdd')
            datestr(QDate.MonthEndsBtw(dt5, dt3),'yyyymmdd')
        end
    end
    
end
