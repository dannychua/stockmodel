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
        return indicatorsData.loc[date, stockID][fieldName]   ## does it have asof ?
    except KeyError:
        print '[__getIndicator]: StockID not found: ', stockID
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
       where TRADE_DT>'%s' """ % GlobalConstant.DataStartDate

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