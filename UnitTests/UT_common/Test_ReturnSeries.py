from nose.tools import with_setup
from nose.tools import assert_equal
from nose.tools import assert_almost_equal
from common.ReturnSeries import ReturnSeries


class TestReturnSeries:

    def setUp(self):
        self.returnSeries = ReturnSeries(['20100101', '20100102', '20100103', '20100104'], [111,222,333,444])

    def tearDown(self):
        pass

    @with_setup(setUp, tearDown)

    def test_annMean(self):
        assert_almost_equal (self.returnSeries.annMean, 1110.0)

    def test_annStd(self):
        assert_almost_equal (self.returnSeries.annStd, 573.201535239)

    def test_sr(self):
        assert_almost_equal (self.returnSeries.sr, 3.87298334621)

    def test_returns(self):
        assert_equal (self.returnSeries.returns, [111, 222, 333, 444])

    def test_compCumReturns(self):
        assert_equal (self.returnSeries.compCumReturns.iloc[-1], 3643368984)