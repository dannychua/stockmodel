import numpy as np
from nose.tools import assert_almost_equal


def test_BPCalc():
	assert_almost_equal (BPCalc('600230.SH', '20140808'), np.float64(0.597657183839), 4)

def test_AllCalc():
	stockID = '600230.SH'
	date = '20140808'
	print('BP, ' + str(BPCalc(stockID, date)))
	print('EP, ' + str(EPCalc(stockID, date)))
	print('EPttm, ' + str(EPttmCalc(stockID, date)))
	print('CFP, ' + str(CFPCalc(stockID, date)))
	print('CFPttm, ' + str(CFPttmCalc(stockID, date)))
	print('OCFP, ' + str(OCFPCalc(stockID, date)))
	print('OCFPttm, ' + str(OCFPttmCalc(stockID, date)))
	print('SalesP, ' + str(SalesPCalc(stockID, date)))
	print('SalesPttm, ' + str(SalesPttmCalc(stockID, date)))
	print('Turnover, ' + str(TurnoverCalc(stockID, date)))
	print('FreeTurnover, ' + str(FreeTurnoverCalc(stockID, date)))
	print('DividendYield, ' + str(DividendYieldCalc(stockID, date)))

if __name__ == '__main__':
    test_AllCalc()
    pass