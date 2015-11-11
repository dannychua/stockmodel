__author__ = 'xiaodan'
import datetime
import pandas as pd
from pandas.tseries.offsets import *
from pandas.tslib import Timestamp

import GlobalConstant
from Utils import Str2Date

# %% header
# % handle a holding and the related logic
# % date: 9/5/2015

#exchange trading dates
__TradingDates = None
def GetAllTradingDays():
    '''
    return trading days since DataStartDate
    Note that Shanghai exchange had different trading dates from Shenzhen in the early period.
    To avoid issues, we set the data start date to be 1998-01-01
    Currently it is very slow to load data series back to 1998.
    As a TEMPORARY solution, we load data since 2009.
    :return: a array of trading days
    '''
    global __TradingDates
    if __TradingDates is None:
        sql = '''select TRADE_DAYS from WindDB.dbo.ASHARECALENDAR where s_info_exchmarket = 'SSE' and TRADE_DAYS>'%s' order by TRADE_DAYS''' % GlobalConstant.DataStartDate
        curs = GlobalConstant.DBCONN_WIND.cursor()
        curs.execute(sql)
        __TradingDates = pd.to_datetime([row[0] for row in curs.fetchall()], format='%Y%m%d')
        curs.close()
        # datastart_date = datetime.datetime(1998, 1, 1)
        # __TradingDates = __TradingDates[dates > datastart_date]
    return __TradingDates


def TradingDaysBTW(startDate, endDate):
    '''
    find all trading trades between startDate and endDate
    startDate and endDate are included if they are trading days
    :param startDate: DateTime or string of "yyyymmdd"
    :param endDate: DateTime or string of "yyyymmdd"
    :return: an array of trading days
    '''
    global __TradingDates
    if __TradingDates is None:
        __TradingDates = GetAllTradingDays()
    startDate = Str2Date(startDate)
    endDate = Str2Date(endDate)
    return __TradingDates[(__TradingDates >= startDate) & (__TradingDates <= endDate)]


def FindTradingDay(dt, shift=0):
    '''
    return the trading day which is equal to dt + shift if dt is a trading date,
    otherwise equal to (dt+0) + shift, where (dt+0) is the trading day prior to dt
    :param dt:  DateTime or string of "yyyymmdd"
    :param shift: the number of trading days, it is an integer, and can be 0, positive or negative;
    :return: a trading day in the format of DateTime or None if it is out of the boundary of the trading day array
    '''
    global __TradingDates
    if __TradingDates is None:
        __TradingDates = GetAllTradingDays()
    dates = __TradingDates
    size = len(dates)
    dt = Str2Date(dt)
    if dt > dates[size-1-shift]:
        return None
    elif dt < dates[max(shift, 0)]:
        return None

    priors = dates[dates <= dt]
    if len(priors) > 0:
        loc = dates.get_loc(priors[-1])
        if 0 <loc + shift < size:
            return dates[loc+shift]
    else:
        return None


def MonthBeginningBtw(startDate, endDate):
    '''
    return all month beginnings between startDate and endDate
    startDate or endDate is included if it is month beginning
    :param startDate: DateTime or string of "yyyymmdd"
    :param endDate: DateTime or string of "yyyymmdd"
    :return: an array of pandas.tslib.Timestamp
    '''
    startDate = Str2Date(startDate)
    endDate = Str2Date(endDate)
    offset = MonthBegin()
    days = []
    if startDate.day == 1:
        dt = startDate
    else:
        dt = startDate + offset
    while dt <= endDate:
        days.append(dt)
        dt += offset
    return pd.to_datetime(days)


def MonthEndsBtw(startDate, endDate):
    '''
    return all month ends between startDate and endDate
    startDate or endDate is included if it is month ends
    :param startDate: DateTime or string of "yyyymmdd"
    :param endDate: DateTime or string of "yyyymmdd"
    :return: an array of pandas.tslib.Timestamp
    '''
    startDate = Str2Date(startDate)
    endDate = Str2Date(endDate)
    offset = MonthEnd()
    days = []
    dt = LastDayOfMonth(startDate)
    while dt <= endDate:
        days.append(dt)
        dt += offset
    return pd.to_datetime(days)


def SaturdayBtw(startDate, endDate):
    '''
    return all week ends between startDate and endDate
    startDate or endDate is included if it is week ends
    :param startDate: DateTime or string of "yyyymmdd"
    :param endDate: DateTime or string of "yyyymmdd"
    :return: an array of pandas.tslib.Timestamp
    '''
    startDate = Str2Date(startDate)
    endDate = Str2Date(endDate)
    dt = startDate
    delta = datetime.timedelta(days=1)
    weekend = set([5])
    days = []
    while dt <= endDate:
        if dt.weekday() in weekend:
            days.append(dt)
        dt += delta
    return pd.to_datetime(days)

# % return the calendar day which is equal to dt + shift
# %
def AddDays(date, shift):
    '''
    return the date which is "shift" apart from "date"
    :param date: DateTime or string of "yyyymmdd"
    :param shift: shift is an integer. It can be 0, positive or negative;
    :return: a dateTime object
    '''
    date = Str2Date(date)
    return date + datetime.timedelta(days=shift)


def LastDayOfMonth(date):
    '''
    return the last day of the same month as "date"
    :param date: DateTime or string of "yyyymmdd"
    :return: a DateTime object
    '''
    date = Str2Date(date)
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)





