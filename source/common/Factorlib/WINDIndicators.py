import sys
import os

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GlobalConstant as GlobalConstant
from Utils import Str2Date


def BPCalc(stockID, date):
    """ Retrieve Book/Price from WINDDB """
    #return __getIndicatorFromDB(stockID, date, "1/s_val_pb_new")
    return __getIndicatorFromDB_All(stockID, date, 'BP')


def EPCalc(stockID, date):
    """ Retrieve Earnings/Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pe")


def EPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Earnings/Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pe_ttm")


def CFPCalc(stockID, date):
    """ Retrieve Net Cash flow / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pcf_ncf")


def CFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Net Cash flow / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pcf_ncfttm")


def OCFPCalc(stockID, date):
    """ Retrieve Operating Cash flow / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pcf_ocf")


def OCFPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Operating Cash flow / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pcf_ocfttm")


def SalesPCalc(stockID, date):
    """ Retrieve Sales / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_ps")


def SalesPttmCalc(stockID, date):
    """ Retrieve trailing twelve month Sales / Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_ps_ttm")


def TurnoverCalc(stockID, date):
    """ Retrieve turnover from WINDDB """
    return __getIndicatorFromDB(stockID, date, "s_dq_turn")


def FreeTurnoverCalc(stockID, date):
    """ Retrieve freeturnover from WINDDB """
    return __getIndicatorFromDB(stockID, date, "s_dq_freeturnover")


def DividendYieldCalc(stockID, date):
    """ Retrieve dividend yield from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_price_div_dps")


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


indicatorsData = None
def __getIndicatorFromDB_All(stockID, date, fieldName):
    """ Retrieve indicators from WINDDB """
    
    global indicatorsData

    from datetime import datetime
    GlobalConstant.TestStartDate = datetime(2014, 12, 31)

    if indicatorsData is None:
        # Query Database
        sqlQuery = """
           select TRADE_DT, s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
            1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
            1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
           from WINDDB.DBO.AShareEODDerivativeIndicator
           where TRADE_DT>'%s' """ % GlobalConstant.TestStartDate
        df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND, parse_dates = {'TRADE_DT':'%Y%m%d'})

        # Create list of df
        dates = df.TRADE_DT.unique()
        dfArray = [df[df['TRADE_DT'] == dt].set_index('StockID') for dt in dates]

        # Create Panel
        indicatorsData = pd.Series(dfArray, index=dates)

    date = Str2Date(date)
    return indicatorsData[date].ix[stockID][fieldName]



def __getIndicatorFromDB_byStockID(stockID, fieldName):
    """ Retrieve indicators from WINDDB """
    
    # Query Database
    sqlQuery = """
       select TRADE_DT, s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
        1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
        1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where s_info_windcode='%s'
       and TRADE_DT>'%s' """ % (stockID, GlobalConstant.TestStartDate)
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND, parse_dates = {'TRADE_DT':'%Y%m%d'})
    df = df.set_index('TRADE_DT')

    return df[fieldName]



def __getIndicatorFromDB_byDate(date, fieldName):
    """ Retrieve indicators from WINDDB """

    # Clean date argument to match TRADE_DT format
    date = date.replace('-', '')
    
    # Query Database
    sqlQuery = """
       select TRADE_DT, s_info_windcode StockID, 1/s_val_pb_new BP, 1/s_val_pe EP, 1/s_val_pe_ttm EPttm, 1/s_val_pcf_ncf CFP,
        1/s_val_pcf_ncfttm CFPttm, 1/s_val_pcf_ocf OCFP, 1/s_val_pcf_ocfttm OCFPttm, 1/s_val_ps SalesP,
        1/s_val_ps_ttm SalesPttm, s_dq_turn Turnover, s_dq_freeturnover FreeTurnover, 1/s_price_div_dps DividendYield
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT='%s' """ % date
    df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND, parse_dates = {'TRADE_DT':'%Y%m%d'})
    df = df.set_index('TRADE_DT')

    return df[fieldName]





print 'Working...'
print __getIndicatorFromDB_byStockID('600230.SH', 'BP')
# print __getIndicatorFromDB_byDate('2015-01-03', 'BP')
# print __getIndicatorFromDB_All('600230.SH', '2015-01-01', 'BP')

