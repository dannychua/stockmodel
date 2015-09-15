__author__ = 'xiaodan'
import GlobalConstant
import pandas as pd
from pandas.tseries.offsets import *
import datetime
from pandas.tslib import Timestamp
# %% header
# % handle a holding and the related logic
# % date: 9/5/2015

def GetAllTradingDays():
    sql = '''select TRADE_DAYS from WindDB.dbo.ASHARECALENDAR where s_info_exchmarket = 'SSE' and TRADE_DAYS>'%s' order by TRADE_DAYS''' % GlobalConstant.TestStartDate
    curs = GlobalConstant.DBCONN_WIND.cursor()
    curs.execute(sql)
    dates = pd.to_datetime([row[0] for row in curs.fetchall()], format='%Y%m%d')
    # for row in curs.fetchall():
    #     days.append(datetime.strptime(row[0], '%Y%m%d'))
    curs.close()
    #
    # dates_df.columns = [x[0] for x in curs.description]
    # #dates = datenum(char(curs.Data),'yyyymmdd');
    #
    # # % Shanghai exchange had different trading dates from Shenzhen
    # # % in the early period. To avoid issues, we set start date to be the first date after 1998-01-01
    # #startDate = datenum('19980101','yyyymmdd');
    start_date = datetime.datetime(1998, 1, 1)
    return dates[dates > start_date]

#% find all trading trades between startDate and endDate
# % including startDate and endDate if they are trading days
#        % startDate and endDate are either datenum or 'yyyymmdd'
def TradingDaysBTW(startDate, endDate):
    return GlobalConstant.TradingDates[(GlobalConstant.TradingDates >= startDate) & (GlobalConstant.TradingDates <= endDate)]

# % find all month beginnings between startDate and endDate
# % including startDate and endDate if they are month beginnings
def MonthBeginningBtw(startDate, endDate):
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

# % find all month ends between startDate and endDate
# % including startDate and endDate if they are month ends
def MonthEndsBtw(startDate, endDate):
    offset = MonthEnd()
    days = []
    dt = last_day_of_month(startDate)
    while dt <= endDate:
        days.append(dt)
        dt += offset
    return pd.to_datetime(days)


# % find all week ends between startDate and endDate
# % including startDate and endDate if they are week ends
def WeekEndsBtw(startDate, endDate):
    #% 1997-12-27, Saturday, 729751
    #% temporary solution; can only handle Sat b/w 1997-12-27 ~ 2015-07-25
    #dates = 729751:7:736170;
    #%c = datestr(b,'yyyymmdd ddd');  %% validation
    dt = startDate
    delta = datetime.timedelta(days=1)
    weekend = set([5, 6])
    days = []
    while dt <= endDate:
        if dt.weekday() in weekend:
            days.append(dt)
        dt += delta
    return pd.to_datetime(days)

# % return the calendar day which is equal to dt + shift
# % shift is an integer, and can be 0, positive or negative;
def AddDays(date, shift):
    return date + datetime.timedelta(days=shift)




# % return the trading day which is equal to dt + shift if dt is a trading date,
# % otherwise equal to (dt+0) + shift, where (dt+0) is the trading day prior to dt?
# % and shift is the number of trading days
# % shift is an integer, and can be 0, positive or negative;
def FindTradingDay(dt, shift=0):
    dates = GlobalConstant.TradingDates
    size = len(dates)
    if dt > Timestamp.max:
        dt = Timestamp.max
    priors = dates[dates <= dt]
    within = True if len(priors) else False
    if within:
        loc = dates.get_loc(priors[-1])
        if 0 <loc + shift < size:
            return dates[loc+shift]
    else:
        delta = dates[0] - dt
        if delta.days <= shift < size:
            return dates[shift]
    return None


def UnionDistinct(dates1, dates2):
    return sorted(set(dates1 + dates2))

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


def UnitTests():
    dt1 = datetime.datetime(1990,1,1)
    dt2 = datetime.datetime(2990,1,1)
    dt3 = datetime.datetime(2015,1,1)
    dt4 = datetime.datetime(2015,1,6)
    for dt in [dt1,dt2,dt3,dt4]:
        print FindTradingDay(dt)
    dt5 = datetime.datetime(2014,6,30)
    print MonthBeginningBtw(dt5, dt3)
    print MonthEndsBtw(dt5, dt3)

if __name__ == '__main__':
    # print GetAllTradingDays()
    # print TradingDaysBTW(datetime.datetime(2013,12,31), datetime.datetime(2014,06,30))
    # print MonthBeginningBtw(datetime.datetime(2013,12,31), datetime.datetime(2014,06,30))
    # print MonthEndsBtw(datetime.datetime(2013,12,31), datetime.datetime(2014,06,30))
    # print WeekEndsBtw(datetime.datetime(2013,12,31), datetime.datetime(2014,06,30))
    # print AddDays(datetime.datetime(2013,12,31), 8)
    #print FindTradingDay(datetime.datetime(2009, 05, 24), 0)
    UnitTests()
    pass




