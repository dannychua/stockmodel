__author__ = 'xiaofeng'
from source.common.Stock import *

# more test cases needed to cover all the biz logic
def test_CalcStockReturns():
    stkid = '600048.SH'
    date = '20090404'
    stk = Stock.ByWindID(stkid)

    ret1 = stk.TotalReturnInRange('20140101', '20141231')
    ret2 = stk.TotalReturnInRange('20000101', '20141231')
    ret3 = stk.TotalReturnInRange('20140101', '20140105')
    price1 = stk.PriceOnDate('20140101')
    price2 = stk.PriceOnDate('20140103')
    mktCap1 = stk.FloatMarketCap('20150112')
    mktCap2 = stk.FloatMarketCap('20140103')

    print stk.WindID
    print stk.Ticker
    print stk.Name
    print ret1
    print ret2
    print ret3
    print price1
    print price2
    print mktCap1
    print mktCap2


test_CalcStockReturns()
