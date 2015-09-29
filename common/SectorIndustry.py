# %% header
# % handle sector or industry or concept
# % date: 8/15/2015
import time
import GlobalConstant
import os
import cPickle
from QTimeSeries import QTimeSeries

class SectorIndustry:
    def __init__(self):
        self.WINDIndustry = None
        WINDIndustryCache = GlobalConstant.DATA_DIR + 'WINDIndustry.dat'
        if os.path.exists(WINDIndustryCache):
            with open(WINDIndustryCache) as fin:
                self.WINDIndustry = cPickle.load(fin)
        else:
            self.WINDIndustry = SectorIndustry.loadWINDIndustry()
            with open(WINDIndustryCache, 'w') as fout:
                cPickle.dump(self.WINDIndustry, fout)


    @staticmethod
    def loadWINDIndustry():
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


