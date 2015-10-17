__author__ = 'xiaofeng'
from source.common.Stock import *
from nose.tools import assert_equal

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

# replace the following print statements with asset_equal
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
# 600048.SH
# 600048
# 保利房地产(集团)股份有限公司
# 31.1515151515
# None
# -1.69696969697
# None
# 8.11
# 111160158480.0
# 57889134511.0

test_CalcStockReturns()
