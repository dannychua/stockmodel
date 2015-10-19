from source.common.QDate import *
from source.common.Utils import *
from pandas import *

def test_tradingDays():
    dt1 = datetime(1990,1,1)
    dt2 = datetime(2016,1,1)
    dt3 = datetime(2015,1,1)
    dt4 = datetime(2015,1,6)
    print type(dt1)
    print type(Str2Date("20150101"))
    for dt in [dt1,dt2,dt3,dt4]:
        print FindTradingDay(dt)
    dt5 = datetime(2014,6,30)
    monBegins = MonthBeginningBtw(dt5, dt3)
    monEnds = MonthEndsBtw(dt5, dt3)
    print monBegins
    print monEnds
    print type(monBegins[0])
    monBeginsDT = [dt.ctime() for dt in monBegins]
    print monBeginsDT
    DT1 = monBeginsDT[0]
    dt1 = pd.to_datetime(DT1, format('%Y%m%d'))
    print DT1
    print dt1
    weekends = SaturdayBtw(dt5, dt3)
    print weekends

    print AddDays(dt3, 10)
    print AddDays(dt3, -10)
    print AddDays(dt3, 0)
    print LastDayOfMonth(dt3)

test_tradingDays()

