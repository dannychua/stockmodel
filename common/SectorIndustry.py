# %% header
# % handle sector or industry or concept
# % date: 8/15/2015
import time
import GlobalConstant
from QTimeSeries import QTimeSeries
# %%
#
# % QDate has the format of yyyymmdd

class SectorIndustry:
    def __init__(self):
        #% WIND sector/industry data
        return SectorIndustry.loadWINDIndustry()

    @staticmethod
    def loadWINDIndustry():
        WINDIndustryCache = 'd:\ChinaA\data\WINDIndustry'
        #%save(WINDIndustryCache, 'WINDIndustry');
        #load(WINDIndustryCache)
        sqlString = 'select S_INFO_WINDCODE, WIND_IND_CODE, ENTRY_DT, REMOVE_DT, CUR_SIGN from WindDB.dbo.ASHAREINDUSTRIESCLASS'
        curs = GlobalConstant.DBCONN_WIND.cursor()
        curs.execute(sqlString)
        windIndustry = {}
        for row in curs.fetchall():
            windID, code, entryDt, removeDt, cur_sign = row
            entryDt = time.strptime(entryDt, '%Y%m%d')
            if windID in windIndustry:
                ts = windIndustry[windID]
                ts.add(entryDt, code)
            else:
                ts = QTimeSeries(entryDt, code);
                windIndustry[windID] = ts
        return windIndustry
