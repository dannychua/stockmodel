import sys
import os

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GlobalConstant as GlobalConstant
from Utils import Str2Date
from Utils import Date2Str
from QDate import FindTradingDay


def BPCalc(stockID, date):
    """ Retrieve Book/Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'BP')


def EPCalc(stockID, date):
    """ Retrieve Earnings/Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'EP')


def EPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Earnings/Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'EPttm')


def CFPCalc(stockID, date):
    """ Retrieve Net Cash flow / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'CFP')


def CFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Net Cash flow / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'CFPttm')


def OCFPCalc(stockID, date):
    """ Retrieve Operating Cash flow / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'OCFP')


def OCFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Operating Cash flow / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'OCFPttm')


def SalesPCalc(stockID, date):
    """ Retrieve Sales / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'SalesP')


def SalesPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Sales / Price from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'SalesPttm')


def TurnoverCalc(stockID, date):
    """ Retrieve turnover from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'Turnover')


def FreeTurnoverCalc(stockID, date):
    """ Retrieve freeturnover from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'FreeTurnover')


def DividendYieldCalc(stockID, date):
    """ Retrieve dividend yield from WINDDB """
    return __getIndicatorFromDB_byDate(stockID, date, 'DividendYield')


def __getIndicatorFromDB(stockID, date, fieldName):
    """ Retrieve indicators from WINDDB """
    ## e.g. fieldName = '1/s_val_pcf_ocfttm'
    sqlQuery = """
       select %s F
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT='%s' and S_INFO_WINDCODE='%s'
		""" % (fieldName, date, stockID)
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    rownum, colnum = df.shape
    if rownum < 1:
        return np.nan
    val = df.iloc[0]['F']
    return val


WindIndicatorsCache = None
def __getIndicatorFromDB_byDate(stockId, date, fieldName):
    '''
        retrieve indicators from WINDDB by date.
        To improve efficiency, the data is only loaded once.
        The data "WindIndicatorsCache" is a pd.Series (time series) of pd.DataFrame (rows are indexed by StockID,
            and columns are indexed by FieldName).
        To get the data item requested, do the following
        1. check if the global variable WindIndicatorsCache is None. If yes, load it from the cache file
        2. get the asof trading day of the input "date"
        3. check whether WindIndicatorsCache has the date
            3.1 if yes, return the data item directly
        4 if not, submit the query and append the data frame to the variable
        5 serialize WindIndicatorsCache to the cache file
        6 return the data item.

    :param stockId: Wind stock id
    :param date: a string with format "yyyymmdd"
    :param fieldName: a string
    :return: a float64
    '''

    tradingDt = Date2Str(FindTradingDay(date))
    global WindIndicatorsCache
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "WindIndicatorsCache.dat"

    if WindIndicatorsCache is None:
        if os.path.exists(cacheFile):
            WindIndicatorsCache = pd.read_pickle(cacheFile)  ## it is a pd.Series with index being date

    if WindIndicatorsCache is None:
        WindIndicatorsCache = pd.TimeSeries()    # the cache file doesn't exist

    if tradingDt in WindIndicatorsCache:
        df = WindIndicatorsCache.ix[tradingDt]           ## should allow AsOf, e.g. allow less than 5 days stale
        if stockId in df.index:
            return df.ix[stockId][fieldName]
        return None

    # either the cache file doesn't exist or the cache doesn't contain the date
    # Query Database
    sqlQuery = """
       select s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
        1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
        1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT='%s' """ % tradingDt
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    df = df.set_index('StockID')
    value = df.ix[stockId][fieldName]

    WindIndicatorsCache[tradingDt] = df
    #pd.to_pickle(WindIndicatorsCache,cacheFile)

    return value

def SaveWindIndicatorsCache():
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "WindIndicatorsCache.dat"
    pd.to_pickle(WindIndicatorsCache,cacheFile)



# print 'Working...'
# print __getIndicatorFromDB_byStockID('600230.SH', 'BP')
# print __getIndicatorFromDB_byDate('2015-01-03', 'BP')
# print __getIndicatorFromDB_All('600230.SH', '2015-01-01', 'BP')

## to be deleted
# indicatorsData = None
# def __getIndicatorFromDB_All(stockID, date, fieldName):
#     """ Retrieve indicators from WINDDB """
#     global indicatorsData
#     # from datetime import datetime
#     # GlobalConstant.TestStartDate = datetime(2014, 12, 31)
#
#     if indicatorsData is None:
#         # Query Database
#         sqlQuery = """
#            select TRADE_DT, s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
#             1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
#             1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
#            from WINDDB.DBO.AShareEODDerivativeIndicator
#            where TRADE_DT>'%s' """ % GlobalConstant.TestStartDate
#         df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND, parse_dates = {'TRADE_DT':'%Y%m%d'})
#
#         # Create list of df
#         dates = df.TRADE_DT.unique()
#         dfArray = [df[df['TRADE_DT'] == dt].set_index('StockID') for dt in dates]
#
#         # Create Panel
#         indicatorsData = pd.Series(dfArray, index=dates)
#
#     date = Str2Date(date)
#     return indicatorsData[date].ix[stockID][fieldName]
#
