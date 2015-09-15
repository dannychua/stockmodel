%% header
% handle sector or industry or concept
% date: 8/15/2015

%%

% QDate has the format of yyyymmdd
classdef SectorIndustry
    properties (Constant)
        % WIND sector/industry data
        WINDIndustry = SectorIndustry.loadWINDIndustry();

    end
    
    methods (Static)  % better be private
        % load WIND sector/industry data from DB
        function windIndustry = loadWINDIndustry()    
            WINDIndustryCache = 'd:\ChinaA\data\WINDIndustry';
            %save(WINDIndustryCache, 'WINDIndustry');
            load(WINDIndustryCache); 
            windIndustry = WINDIndustry;
            return;
            
            sqlString = 'select S_INFO_WINDCODE, WIND_IND_CODE, ENTRY_DT, REMOVE_DT, CUR_SIGN from WindDB.dbo.ASHAREINDUSTRIESCLASS';
            curs = exec(GlobalConstant.DBCONN_WIND, sqlString);
            curs = fetch(curs);
            len = length(curs.Data);            
            windIndustry = containers.Map();
            for i = 1:len
                windID = curs.Data{i,1};

                code = curs.Data{i,2};              
                entryDt = datenum(curs.Data{i,3}, 'yyyymmdd');
                
                if (isKey(windIndustry, windID))
                    ts = values(windIndustry,{windID});
                    ts = ts{1};
                    Add(ts, entryDt, code);
                else
                    ts = QTimeSeries(entryDt, {code});
                    windIndustry = [windIndustry; containers.Map(windID, ts)];
                end
            end
            clear curs;                
        end        

    end
    
end
