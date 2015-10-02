from common.PortfolioProviders import PortfolioProviders


def test_getClosingPx():
	closingPx_ts = PortfolioProviders.getClosingPx('000016.SH')
	assert closingPx_ts.qseries.iloc[0] == 1436.885


def test_getA50():
	portfolioProvider = PortfolioProviders.getA50()
	portfolio = portfolioProvider.GetPortfolioOn('20090401')
	holdings = portfolio.getHoldings()
	assert holdings[0] == {'Weight': 0.274, 'StockID': '601991.SH'}