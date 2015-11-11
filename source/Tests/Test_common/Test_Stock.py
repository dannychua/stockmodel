# -*- coding: utf-8 -*-
__author__ = 'xiaofeng'
from source.common.Stock import *
from nose.tools import assert_equal

def test_CalcStockReturns():
    stkid = '600048.SH'
    stk = Stock.ByWindID(stkid)
    print stkid
    # print [stk.ShortName, stk.Name]   # can't print Chinese characters
    print stk.ShortName
    print stk.Name
    print [stk.Exchange, stk.ListBoard, stk.ListDate]

    date0 = Str2Date('20131231')
    date1 = Str2Date('20140101')  # New Year Holiday
    date2 = Str2Date('20140102')
    date3 = Str2Date('20140111')  # Saturday

    price0 = stk.UnAdjPrice(date0)
    adjPrice0 = stk.AdjClosingPx.ValueOn(date0)
    adjVWAPPrice0 = stk.AdjVWAP.ValueOn(date0)
    print [round(price0,2), round(adjPrice0,2), round(adjVWAPPrice0,2)]

    price1 = stk.UnAdjPrice(date1)
    adjPrice1Asof = stk.AdjClosingPx.ValueAsOf(date1)
    adjVWAPPrice1Asof = stk.AdjVWAP.ValueAsOf(date1)
    adjPrice1After = stk.AdjClosingPx.ValueAfter(date1)
    adjVWAPPrice1After = stk.AdjVWAP.ValueAfter(date1)
    print [price1, round(adjPrice1Asof,2), round(adjVWAPPrice1Asof,2), round(adjPrice1After,2), round(adjVWAPPrice1After,2)]

    price2 = stk.UnAdjPrice(date2)
    adjPrice2 = stk.AdjClosingPx.ValueOn(date2)
    adjVWAPPrice2 = stk.AdjVWAP.ValueOn(date2)
    print [round(price2,2), round(adjPrice2,2), round(adjVWAPPrice2,2)]

    ret0 = stk.TotalReturnInRange(date0, date3)
    ret1 = stk.TotalReturnInRange(date1, date3)
    print [round(ret0,2), round(ret1,2)]

    ret0VWAP = stk.TotalReturnInRange_VWAP(date0, date3)
    ret1VWAP = stk.TotalReturnInRange_VWAP(date1, date3)
    print [round(ret0VWAP,2), round(ret1VWAP,2)]

    ret0bk = stk.TotalReturnInRange_VWAP_Bk(date0, date3)
    ret1bk = stk.TotalReturnInRange_VWAP_Bk(date1, date3)
    print [round(ret0bk,2), round(ret1bk,2)]

    mktCap0 = stk.FloatMarketCap(date0)
    mktCap1 = stk.FloatMarketCap(date1)
    print [mktCap0, mktCap1, mktCap1-mktCap0]

# output =======================
# 600048.SH
# 保利地产
# 保利房地产(集团)股份有限公司
# ['SSE', '434004000', '20060731']
# [8.25, 92.57, 91.4]
# [None, 92.57, 91.4, 91.78, 91.81]
# [8.18, 91.78, 91.81]
# [-7.15, -7.15]
# [-5.9, -5.9]
# [-8.0, -8.4]
# [58888453725.75, 58888453725.75, 0.0]

def test_IndustrySectorCode():
    stkid = '600048.SH'
    stk = Stock.ByWindID(stkid)
    date1 = Str2Date('20140101')  # New Year Holiday
    sector = stk.WindSectorCode(date1)
    industry = stk.WindIndustryCode(date1)
    print [sector, industry]

#test_CalcStockReturns()
test_IndustrySectorCode()
