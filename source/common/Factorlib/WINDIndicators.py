import sys
import os

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GlobalConstant as GlobalConstant
from Utils import Date2Str
from QDate import FindTradingDay


def BPCalc(stockID, date):
    """ Retrieve Book/Price from WINDDB """
    return __getIndicator(stockID, date, 'BP')


def EPCalc(stockID, date):
    """ Retrieve Earnings/Price from WINDDB """
    return __getIndicator(stockID, date, 'EP')


def EPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Earnings/Price from WINDDB """
    return __getIndicator(stockID, date, 'EPttm')


def CFPCalc(stockID, date):
    """ Retrieve Net Cash flow / Price from WINDDB """
    return __getIndicator(stockID, date, 'CFP')


def CFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Net Cash flow / Price from WINDDB """
    return __getIndicator(stockID, date, 'CFPttm')


def OCFPCalc(stockID, date):
    """ Retrieve Operating Cash flow / Price from WINDDB """
    return __getIndicator(stockID, date, 'OCFP')


def OCFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Operating Cash flow / Price from WINDDB """
    return __getIndicator(stockID, date, 'OCFPttm')


def SalesPCalc(stockID, date):
    """ Retrieve Sales / Price from WINDDB """
    return __getIndicator(stockID, date, 'SalesP')


def SalesPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Sales / Price from WINDDB """
    return __getIndicator(stockID, date, 'SalesPttm')


def TurnoverCalc(stockID, date):
    """ Retrieve turnover from WINDDB """
    return __getIndicator(stockID, date, 'Turnover')


def FreeTurnoverCalc(stockID, date):
    """ Retrieve freeturnover from WINDDB """
    return __getIndicator(stockID, date, 'FreeTurnover')


def DividendYieldCalc(stockID, date):
    """ Retrieve dividend yield from WINDDB """
    return __getIndicator(stockID, date, 'DividendYield')





# Loading of this module will cause the creation of this cache
indicatorsData = None

def __getIndicator(stockID, date, fieldName, purgeCache=False):
    """ Retrieve all indicators from WINDDB """
    
    global indicatorsData

    # If cache not in memory
    if (indicatorsData is None) or (purgeCache == True):
        # Handle cache purge
        if purgeCache == True:
            indicatorsData = None
            print 'indicatorsData purged'

        print 'indicatorsData not in memory'

        # Try the HDFStore Cache
        hdfPath = os.path.join(GlobalConstant.DATA_DIR, 'db.h5')
        store = pd.HDFStore(hdfPath)

        # If cache not in HDFStore
        if ('df_indicators' not in store) or (purgeCache == True):
            print 'indicatorsData not in HDFStore'

            # Dump indicators from DB to HDFStore
            __writeAllIndicatorsFromDbToHDFStore(store)

            # Reindex store['df_indicators']
            __reindexIndicatorsHDFStore()

        # Hit the HDFStore cache
        indicatorsData = store.get('df_indicators') 
        print 'df_indicators loaded from disk cache'
        store.close()

        try:
            return indicatorsData.loc[date, stockID][fieldName]
        except KeyError:
            print '[__getIndicator]: StockID not found: ', StockID
            return np.NaN


def  __writeAllIndicatorsFromDbToHDFStore(store):
    """ Retrieve all Indicator data from database and write to HDFStore """

    # Start with a clean empty DataFrame
    store.put('df_indicators', pd.DataFrame(), 'table')   

    # Query Database
    sqlQuery = """
       select TRADE_DT, s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
        1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
        1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT>'%s' """ % GlobalConstant.TestStartDate

    # SELECT from DB in chunks,
    # persist chunk to disk before retriving next chunk from DB
    for chunk in pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND, parse_dates = {'TRADE_DT':'%Y%m%d'}, chunksize=10000):
        
        # Convert None to NaN since Pandas cant tell dtypes if entire column retrieved from database are NULLs
        df = chunk.fillna(value=np.nan).set_index('TRADE_DT')

        # Persist to HDF5 Store
        store.append('df_indicators', df)

    return


def __reindexIndicatorsHDFStore():
    """ Rebuild df_indicators to enable MultiIndex DataFrame data structure """

    # Load df from HDFStore
    hdfPath = os.path.join(GlobalConstant.DATA_DIR, 'db.h5')
    store = pd.HDFStore(hdfPath)
    df = store.get('df_indicators')    

    # Reset index to col (index must be set previously during read_sql step of creating .h5 store's df for SQL retrival by chunk)
    df.reset_index(inplace=True)

    # Reindex with MultiIndex
    df = df.set_index(['TRADE_DT', 'StockID']).sortlevel()

    # Persist to HDFStore and close
    store.put('df_indicators', df)
    store.close()











def _getEODDerivativeIndicatorFromDB(stockID, date, fieldName):
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

EODDerivativeIndicatorCache = None
def _getEODDerivativeIndicatorFromDB_byDate(stockId, date, fieldName):
    '''
        retrieve indicators from WINDDB by date.
        To improve efficiency, the data is only loaded once.
        The data "EODDerivativeIndicatorCache" is a pd.Series (time series) of pd.DataFrame (rows are indexed by StockID,
            and columns are indexed by FieldName).
        To get the data item requested, do the following
        1. check if the global variable EODDerivativeIndicatorCache is None. If yes, load it from the cache file
        2. get the asof trading day of the input "date"
        3. check whether EODDerivativeIndicatorCache has the date
            3.1 if yes, return the data item directly
        4 if not, submit the query and append the data frame to the variable
        5 serialize EODDerivativeIndicatorCache to the cache file
        6 return the data item.

    :param stockId: Wind stock id
    :param date: a string with format "yyyymmdd"
    :param fieldName: a string
    :return: a float64
    '''

    tradingDt = Date2Str(FindTradingDay(date))
    global EODDerivativeIndicatorCache
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EODDerivativeIndicatorCache.dat"

    if EODDerivativeIndicatorCache is None:
        if os.path.exists(cacheFile):
            EODDerivativeIndicatorCache = pd.read_pickle(cacheFile)  ## it is a pd.Series with index being date

    if EODDerivativeIndicatorCache is None:
        EODDerivativeIndicatorCache = pd.TimeSeries()    # the cache file doesn't exist

    if tradingDt in EODDerivativeIndicatorCache:
        df = EODDerivativeIndicatorCache.ix[tradingDt]           ## should allow AsOf, e.g. allow less than 5 days stale
        if stockId in df.index:
            return df.ix[stockId][fieldName]
        return np.nan

    # we get to this point, so either the cache file doesn't exist or the cache doesn't contain the date
    # then query database
    sqlQuery = """
       select s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
        1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
        1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT='%s' """ % tradingDt
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
    df = df.set_index('StockID')
    value = df.ix[stockId][fieldName]

    EODDerivativeIndicatorCache[tradingDt] = df
    if value is None:
        return np.nan
    else:
        return value

def SaveEODDerivativeIndicatorCache():
    cacheFile = GlobalConstant.DATA_FactorScores_DIR + "EODDerivativeIndicatorCache.dat"
    pd.to_pickle(EODDerivativeIndicatorCache,cacheFile)