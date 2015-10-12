from nose.tools import assert_equal

from source.common import PortfolioProviders


def test_getClosingPx():
	closingPx_ts = PortfolioProviders.getClosingPx('000016.SH')
	assert_equal(closingPx_ts.Timeseries.iloc[0], 1436.885)


def test_getA50():
	portfolioProvider = PortfolioProviders.getA50()
	portfolio = portfolioProvider.GetPortfolioOn('20090401')
	holdings = portfolio.Holdings
	assert_equal(len(holdings), 50)
	stockID = '601991.SH'
	wt = portfolio.WeightOfStock(stockID)   ### the order of stocks is uncertain
	assert_equal((wt, stockID), (0.274, '601991.SH'))

test_getA50()
test_getClosingPx()