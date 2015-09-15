%% header
% retrieve Book/Price from WINDDB
% Date: 7/3/2015

%%
% date is either datenum or datestr in the format of yyyymmdd
function [score] = BPCalc(stockID, date)
    if(isnumeric(date))
        date = datestr(date,'yyyymmdd');
    end
    stkid = stockID;
    sqlString = [...
                   'select 1/s_val_pb_new ''BP''' char(10)...   
                   'from WINDDB.DBO.AShareEODDerivativeIndicator' char(10)...
                   'where TRADE_DT=''',date,''' and S_INFO_WINDCODE=''', stkid, '''' char(10)...                   
                   ];                   
    curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
    curs = fetch(curs);    
    score = curs.Data{1};    % return double, not cell
    if(length(score)>1)
        score = nan;   % the query sometimes returns 'No Data'
    end
    clear curs;    
end