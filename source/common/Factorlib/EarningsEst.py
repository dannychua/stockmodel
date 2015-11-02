__author__ = 'xiaofeng'
import os
import numpy as np
import pandas as pd

import source.common.GlobalConstant as GlobalConstant
from source.common.Utils import Date2Str
from source.common.QDate import FindTradingDay

EarningEstCache = None
#todo
def _getEarningEstFromDB_byDate(stockId, date, fieldName):
    '''
    :param stockId: Wind stock id
    :param date: a string with format "yyyymmdd"
    :param fieldName: a string
    :return: a float64
    '''

    tradingDt = Date2Str(FindTradingDay(date))
    global EarningEstCache
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EarningEstCache.dat"

    if EarningEstCache is None:
        if os.path.exists(cacheFile):
            EarningEstCache = pd.read_pickle(cacheFile)  ## it is a pd.Series with index being date

    if EarningEstCache is None:
        EarningEstCache = pd.TimeSeries()    # the cache file doesn't exist

    if tradingDt in EarningEstCache:
        df = EarningEstCache.ix[tradingDt]           ## should allow AsOf, e.g. allow less than 5 days stale
        if stockId in df.index:
            return df.ix[stockId][fieldName]
        return np.nan

    # we get to this point, so either the cache file doesn't exist or the cache doesn't contain the date
    # then query database
    sqlQuery = """
         select S_INFO_WINDCODE, EST_DT, EST_REPORT_DT, S_EST_YEARTYPE, CONSEN_DATA_CYCLE_TYP, EPS_AVG, ebitda_avg/S_EST_BASESHARE EBITDA_AVG, s_est_avgcps CPS_AVG, s_est_avgdps DPS_AVG, s_est_avgbps BPS_AVG, s_est_avgroa ROA_AVG, s_est_avgoperatingprofit/S_EST_BASESHARE OPProfit_AVG
  from WindDB.dbo.AShareConsensusData
  -- where S_INFO_WINDCODE = '600048.SH'
  -- order by est_dt
  --where EST_DT = '20150109' and CONSEN_DATA_CYCLE_TYP = '263001000'
  where EST_DT > '20150101' and EST_DT <= '20150109' and CONSEN_DATA_CYCLE_TYP = '263002000' and S_EST_YEARTYPE = 'FY2'
       where TRADE_DT='%s' """ % tradingDt
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    df = df.set_index('StockID')
    value = df.ix[stockId][fieldName]

    EarningEstCache[tradingDt] = df
    if value is None:
        return np.nan
    else:
        return value

def SaveEarningEstCache():
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EarningEstCache.dat"
    pd.to_pickle(EarningEstCache,cacheFile)


