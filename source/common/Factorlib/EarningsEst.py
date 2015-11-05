__author__ = 'xiaofeng'
import os
import numpy as np
import pandas as pd

import source.common.GlobalConstant as GlobalConstant
from source.common.Utils import Date2Str
from source.common.QDate import FindTradingDay


def PEFY2Calc(stockId, date):
    return _getEarningEstFromDB_byDate(stockId, date)

EarningEstCache = None
#todo
def _getEarningEstFromDB_byDate(stockId, date, fieldName = 'EPS_AVG'):
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
        EarningEstCache = pd.Series()    # the cache file doesn't exist

    if tradingDt in EarningEstCache:
        df = EarningEstCache.ix[stockId]           ## should allow AsOf, e.g. allow less than 5 days stale
        if tradingDt in df.index:
            dt = pd.to_datetime(df.index, format('%Y%m%d')).asof(tradingDt) ## find dt using asof
            dt = Date2Str(dt)
            return df.ix[dt][fieldName]
        return np.nan

    # we get to this point, so either the cache file doesn't exist or the cache doesn't contain the date
    # then query database
    #     S_EST_YEARTYPE: FY1, FY2 and FY3
    #     CONSEN_DATA_CYCLE_TYP 263001000: 30 days, 263001000: 90 days, 263001000: 180 days
    #     each row os the table represents a sell side analyst issues a forecast
    #     on any given date, only small portion of stocks would have data
    #     given a stock and a date, the goal is to find the most recent row (consensus forecast) up to that date
    #     all per-share-fields are non-split-adjusted  (not confirmed!!!)
    #     EPS_AVG would never be Null
    #     other fields might be Null
    #     deal with EPS_AVG first and then extend to other fields

    dataStartDt = Date2Str(GlobalConstant.TestStartDate)
    sqlQuery = """
        select EST_DT, EPS_AVG
        from WindDB.dbo.AShareConsensusData
        where S_INFO_WINDCODE = '%s' and EST_DT>'%s' and CONSEN_DATA_CYCLE_TYP = '263002000' and S_EST_YEARTYPE = 'FY2'
        order by est_dt
        """ % (stockId, dataStartDt)
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    df = df.set_index('EST_DT')        ## should set the index to DateTimeIndex here avoiding transformation later
    dt = pd.to_datetime(df.index, format('%Y%m%d')).asof(tradingDt)  ## find dt using asof, time consuming
    dt = Date2Str(dt)
    value = df.ix[dt][fieldName]

    EarningEstCache[stockId] = df
    if value is None:
        return np.nan
    else:
        return value

def SaveEarningEstCache():
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EarningEstCache.dat"
    pd.to_pickle(EarningEstCache,cacheFile)


