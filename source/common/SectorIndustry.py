# %% header
# % handle sector or industry or concept
# % date: 8/15/2015
import time
import GlobalConstant
import os
import cPickle
import collections
from QTimeSeries import QTimeSeries
from Utils import Str2Date

class SectorIndustry:
    WINDIndustry = None
    def __init__(self):
        self.WINDIndustry = SectorIndustry.loadWINDIndustry()
        #WINDIndustryCache = GlobalConstant.DATA_DIR + 'WINDIndustry.dat'
        # if os.path.exists(WINDIndustryCache):
        #     with open(WINDIndustryCache) as fin:
        #         self.WINDIndustry = cPickle.load(fin)
        # else:
        #     self.WINDIndustry = SectorIndustry.loadWINDIndustry()
        #     with open(WINDIndustryCache, 'w') as fout:
        #         cPickle.dump(self.WINDIndustry, fout)


    @staticmethod
    def loadWINDIndustry():
        sqlString = 'select S_INFO_WINDCODE, WIND_IND_CODE, ENTRY_DT, REMOVE_DT, CUR_SIGN from WindDB.dbo.ASHAREINDUSTRIESCLASS order by ENTRY_DT'
        curs = GlobalConstant.DBCONN_WIND.cursor()
        curs.execute(sqlString)
        windIndustry_tmp = collections.defaultdict(list)
        for row in curs.fetchall():
            windID, code, entryDt, removeDt, cur_sign = row
            entryDt = Str2Date(entryDt)
            removeDt = Str2Date(removeDt)
            windIndustry_tmp[windID].append([entryDt, code])
        windIndustry = {}
        for windID, vals in windIndustry_tmp.iteritems():
            dates = []
            codes = []
            for val in vals:
                entryDt, code = val
                dates.append(entryDt)
                codes.append(code)
            windIndustry[windID] = QTimeSeries(dates=dates, values=codes)
        return windIndustry


