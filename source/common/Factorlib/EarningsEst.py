__author__ = 'xiaofeng'
import os
import numpy as np
import pandas as pd
import logging as logging

import source.common.GlobalConstant as GlobalConstant
from source.common.Utils import Date2Str
from source.common.Utils import Str2Date
from source.common.QDate import FindTradingDay
from source.common.Stock import Stock
from pandas.core.index import InvalidIndexError


def EPFY2Calc(stockId, date):
    return _getEarningEstFromDB_byDate(stockId, date)

#EarningEstCache = None
def getEarningsEstFromDB_Bk():
    MaxLagDays = 120   ## shall it be a GlobalConstant ??

    #startDt = GlobalConstant.DataStartDate
    startDt = '20140131'
    fieldName = 'EPS_AVG'

    ## EST_REPORT_DT is not needed if Type has no data error.
    ## However, there are data errors,e.g.  ['000629.SZ', '2009-04-03']
    sqlQuery = """
        select S_INFO_WINDCODE Ticker, EST_DT, EPS_AVG, S_EST_YEARTYPE Type
        from WindDB.dbo.AShareConsensusData
        where EST_DT>'%s' and CONSEN_DATA_CYCLE_TYP = '263002000'
        order by est_dt
        """ % startDt
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    stockIDs = np.unique(df.Ticker.tolist())

    # dictionary of data frame with stockID being the key
    EarningEstCacheFY1 = {}
    EarningEstCacheFY2 = {}
    EarningEstCacheFY3 = {}

    for stockId in stockIDs:
        dfByStk = df[df.Ticker == stockId]

        EPFY1 = _getFYFromDataFrame(stockId, dfByStk, 'FY1', fieldName)
        EPFY2 = _getFYFromDataFrame(stockId, dfByStk, 'FY2', fieldName)
        EPFY3 = _getFYFromDataFrame(stockId, dfByStk, 'FY3', fieldName)

        EarningEstCacheFY1[stockId] = EPFY1
        EarningEstCacheFY2[stockId] = EPFY2
        EarningEstCacheFY3[stockId] = EPFY3


def _getFYFromDataFrame(stockId, dfByStk, type, fieldName):
    maxLagDays = 120
    dfByStkFY = dfByStk[dfByStk.Type == type]
    ###     the following is wrong!!!
    ### I am trying to set Est_DT as index of the dataframe, and then use asof to get the estDt
    estDts = pd.to_datetime(dfByStkFY['EST_DT'], format('%Y%m%d'))  # rows are sorted by EST_DT
    data = pd.Series(pd[fieldName],index=estDts)

    EPFY = pd.TimeSeries()
    earningEstFY = np.nan
    for dt in GlobalConstant.BacktestDates:
        try:
            estDt = data.index.asof(dt)  # found the Est_Dt using AsOf
        except InvalidIndexError:
            logging.error('Data Error: ' + stockId + ', ' + Date2Str(dt))
            estDt = Str2Date("19000101")

        if estDt is not np.nan and (dt-estDt).days < maxLagDays:   # discard it if it is too stale
            earningEstFY = dfByStkFY.ix[estDt][fieldName]   # is this number (earning forecast) an annual number?
            px = Stock.ByWindID(stockId).UnAdjPrice(estDt)
            EPFY[dt] = earningEstFY/px

    return EPFY


#todo
def _getEarningEstFromDB_byDate(stockId, date, fieldName = 'EPS_AVG'):
    '''
    :param stockId: Wind stock id
    :param date: a string with format "yyyymmdd"
    :param fieldName: a string
    :return: a float64
    '''

    MaxLagDays = 120   ## shall it be a GlobalConstant ??
    value = np.nan

    tradingDt = FindTradingDay(date)
    tradingDtStr = Date2Str(tradingDt)
    global EarningEstCache
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EarningEstCache.dat"

    if EarningEstCache is None:
        if os.path.exists(cacheFile):
            EarningEstCache = pd.read_pickle(cacheFile)  ## it is a pd.Series with index being date

    if EarningEstCache is None:
        EarningEstCache = pd.Series()    # the cache file doesn't exist

    if stockId in EarningEstCache:
        df = EarningEstCache.ix[stockId]           ## should allow AsOf, e.g. allow less than 5 days stale
        if tradingDt in df.index:
            dt = df.index.asof(tradingDt)
            if(tradingDt - dt < MaxLagDays):      # discard it if it is too stale
                value = df.ix[dt][fieldName]
                px = Stock.ByWindID(stockId).UnAdjPrice(dt)
                ep = value/px
                return ep
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

    dataStartDt = GlobalConstant.DataStartDate
    sqlQuery = """
        select EST_DT, EPS_AVG, EST_REPORT_DT
        from WindDB.dbo.AShareConsensusData
        where S_INFO_WINDCODE = '%s' and EST_DT>'%s' and CONSEN_DATA_CYCLE_TYP = '263002000' and S_EST_YEARTYPE = 'FY2'
        order by est_dt
        """ % (stockId, dataStartDt)
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    #GlobalConstant.DBCONN_WIND.close()
    df = df.set_index(pd.to_datetime(df['EST_DT'], format('%Y%m%d')))
    try:
        dt = df.index.asof(tradingDt)
    except InvalidIndexError:
        logging.error('Data Error: ' + stockId + ', ' + Date2Str(tradingDt))
        dt = "19000101"
        #df = df.drop_duplicates(subset='EST_DT', keep='last', inplace=True)  ## argument keep only works with v0.17.0
        df.drop_duplicates(subset='EST_DT', inplace=True)  ## the current version of pd is v0.16.2
        dt = df.index.asof(tradingDt)   ## to reproduce the InvalidIndexError.  it is likely a data error, e.g. ['000629.SZ', '2009-04-03']

    if dt is not np.nan and (tradingDt - dt).days < MaxLagDays:   # discard it if it is too stale
        value = df.ix[dt][fieldName]   # is this number (earning forecast) an annual number?
        px = Stock.ByWindID(stockId).UnAdjPrice(dt)
        value = value/px

    EarningEstCache[stockId] = df
    return value


def SaveEarningEstCache():
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EarningEstCache.dat"
    pd.to_pickle(EarningEstCache,cacheFile)


