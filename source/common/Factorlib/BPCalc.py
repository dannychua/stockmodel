import sys
import os

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GlobalConstant as GlobalConstant


def BPCalc(stockID, date):
    """ Retrieve Book/Price from WINDDB """
    return __getIndicatorFromDB(stockID, date, "1/s_val_pb_new")


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
