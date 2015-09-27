import numpy as np
from Utils import checkDate
from Stock import Stock
import sys
# %% header
# % handle a portfolio and the related logic
# % a portfolio is a set of holdings with a date when the portfolio is
# % evaluated
# % date: 7/3/2015
#
# %%
# % it is a handle class

class Portfolio:

    def __init__(self):
        self.Date = None         # the date on which the portfolio is evaluated
        self.Holdings = []       # the stocks held and their weights in the portfolio, could be empty
        self.MarketValue = None  # the market value of the portfolio, could be negative or null

    #% holdings could be empty
    #% dim is the length of the portfolio array, used to initiate an array of portfolios
    #% to be implemented: it'd better remove 'dim' as a parameter
    def __init__(self, date, holdings=[]):
        self.Date = date
        if len(holdings):
            self.Holdings = holdings


    def Portfolio(self, date, holdings=[]):
        self.Date = date
        if len(holdings):
            self.Holdings = holdings

    def AddHolding(self, holding):
        self.Holdings.append(holding)

    #% re-weight the portfolio to be equal weighted
    def ReWeightEqual(self):
        if len(self.Holdings):   # % if the portfolio has holdings
            wt = 100.0/len(self.Holdings)
            for i in xrange(len(self.Holdings)):
                self.Holdings[i].Weight = wt

    #% re-weight the long side to be 100%
    def ReWeightTo100(self):
        if len(self.Holdings):    #% if the portfolio has holdings
            wts = np.array([x.Weight for x in self.Holdings])
            total = wts[wts>0].sum()   #% sum the positive weights only
            scalar = 100.0/total
            for i in xrange(len(self.Holdings)):
                self.Holdings[i].Weight *= scalar


    #% market cap is evaluated as of 'date'
    def ReWeightMarketCap(self):
        if len(self.Holdings):   #% if the portfolio has holdings
            size = len(self.Holdings)
            mktCaps = np.zeros(size) #% note that Weights is 1 X n
            total = 0
            for i in xrange(size):
                stk = Stock.ByWindID(self.Holdings[i].StockID)
                mktCaps[i] = stk.FloatMarketCap(self.Date)
                if np.isnan(mktCaps[i]):
                    mktCaps[i] = 0
                total +=  mktCaps[i]
            for i in xrange(size):
                self.Holdings[i].Weight = 100.0*mktCaps[i]/total

        # % hold the portfolio obj through "date"
        # % if reweightTo100 = true, the total long weight is 100%
        # % otherwise (default), don't reweight it
    def  HeldToDate(self, date, reweightTo100):
            if self.Date < date and len(self.Holdings):
                size = len(self.Holdings)
                for i in xrange(size):
                    stk = Stock.ByWindID(self.Holdings[i].StockID)
                    ret = stk.TotalReturnInRange(self.Date, date)
                    if np.isnan(ret):
                        ret = 0
                    self.Holdings[i].Weight = self.Holdings[i].Weight*(1+0.01*ret)
                if reweightTo100:
                    self.ReWeightTo100()

        # % calculate total returns of the portfolio from startDate to endDate
        # % pfReturn is in percentage
    def TotalReturnInRange(self, startDate, endDate):
            startDate = checkDate(startDate)
            endDate = checkDate(endDate)
            pfReturn = 0
            validWt = 0
            numHoldings = len(self.Holdings)
            for i in xrange(numHoldings):
                stk = Stock.ByWindID(self.Holdings[i].StockID)
                stkRet = stk.TotalReturnInRange(startDate, endDate)
                if stkRet and not np.isnan(stkRet):
                    validWt = validWt + self.Holdings[i].Weight
                    pfReturn = pfReturn + stkRet * self.Holdings[i].Weight * 0.01
            if validWt < 95:
                print >> sys.stderr, 'less than 95% of the portfolio has valid returns'

    def GetStockIDs(self):
        return str(self.Holdings.StockID)

    def getHoldings(self):
        return self.Holdings
