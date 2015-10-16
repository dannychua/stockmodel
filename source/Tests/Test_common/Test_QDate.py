from source.common.QDate import *

def UnitTests():
    dt1 = datetime.datetime(1990,1,1)
    dt2 = datetime.datetime(2990,1,1)
    dt3 = datetime.datetime(2015,1,1)
    dt4 = datetime.datetime(2015,1,6)
    for dt in [dt1,dt2,dt3,dt4]:
        print FindTradingDay(dt)
    dt5 = datetime.datetime(2014,6,30)
    monBegins = MonthBeginningBtw(dt5, dt3)
    monEnds = MonthEndsBtw(dt5, dt3)
    print monBegins
    print monEnds
    monBeginsDT = [dt.ctime() for dt in monBegins]
    print monBeginsDT
    DT1 = monBeginsDT[0]
    dt1 = pd.to_datetime(DT1, format('%Y%m%d'))
    print DT1
    print dt1


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
