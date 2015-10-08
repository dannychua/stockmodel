from nose.tools import assert_equal
from common.PortfolioProviders import PortfolioProviders


def test_getClosingPx():
	closingPx_ts = PortfolioProviders.getClosingPx('000016.SH')
	assert_equal(closingPx_ts.Series.iloc[0], 1436.885)


def test_getA50():
	portfolioProvider = PortfolioProviders.getA50()
	portfolio = portfolioProvider.GetPortfolioOn('20090401')
	holdings = portfolio.Holdings
	holding = holdings[0]
	assert_equal((holding.Weight, holding.StockID), (0.274, '601991.SH'))