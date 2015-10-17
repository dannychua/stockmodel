import numpy as np
from nose.tools import with_setup
from nose.tools import assert_almost_equal
from source.common.Factorlib.BPCalc import *



class TestBPCalc:

    def setUp(self):
        self.stockID = '600230.SH'
        self.date = '20140808'

    @with_setup(setUp)

    def test_BPCalc(self):
        assert_almost_equal (BPCalc('600230.SH', '20140808'), np.float64(0.597657183839), 4)

    def test_EPCalc(self):
        assert_almost_equal (EPCalc(self.stockID, self.date), np.float64(0.0376256697369), 4)

    def test_EPttmCalc(self):
        assert_almost_equal (EPttmCalc(self.stockID, self.date), np.float64(0.0318692595496), 4)

    def test_CFPCalc(self):
        assert_almost_equal (CFPCalc(self.stockID, self.date), None)

    def test_CFPttmCalc(self):
        assert_almost_equal (CFPttmCalc(self.stockID, self.date), None)

    def test_OCFPCalc(self):
        assert_almost_equal (OCFPCalc(self.stockID, self.date), np.float64(0.214758182287), 4)

    def test_OCFPttmCalc(self):
        assert_almost_equal (OCFPttmCalc(self.stockID, self.date), np.float64(0.145609155904), 4)

    def SalesPCalc(self):
        assert_almost_equal (SalesPCalc(self.stockID, self.date), np.float64(1.07009095773), 4)

    def test_SalesPttmCalc(self):
        assert_almost_equal (SalesPttmCalc(self.stockID, self.date), np.float64(1.07480653482), 4)

    def test_TurnoverCalc(self):
        assert_almost_equal (TurnoverCalc(self.stockID, self.date), np.float64(2.3805), 4)

    def test_FreeTurnoverCalc(self):
        assert_almost_equal (FreeTurnoverCalc(self.stockID, self.date), np.float64(4.8823), 4)

    def test_DividendYieldCalc(self):
        assert_almost_equal (DividendYieldCalc(self.stockID, self.date), np.float64(0.00397437324134), 4)

if __name__ == '__main__':
    # test_AllCalc()
    # pass
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