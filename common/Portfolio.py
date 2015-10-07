import numpy as np
from Utils import Str2Date
from Stock import Stock
from Holding import Holding
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
    #% holdings could be empty
    #% dim is the length of the portfolio array, used to initiate an array of portfolios
    #% to be implemented: it'd better remove 'dim' as a parameter
    def __init__(self, date, holdings=[]):
        self.Date = date
        if len(holdings):
            holding_new = holdings
            if type(holdings[0]) is dict:
                holding_new = [Holding(holding) for holding in holdings]
            self.__Holdings = holding_new

    def AddHolding(self, holding):
        if type(holding) is dict:
            self.__Holdings.append(Holding(holding))
        else:
            self.__Holdings.append(holding)

    #% re-weight the portfolio to be equal weighted
    def ReWeightEqual(self):
        if len(self.__Holdings):   # % if the portfolio has holdings
            wt = 100.0/len(self.__Holdings)
            for i in xrange(len(self.__Holdings)):
                self.__Holdings[i].Weight = wt

    #% re-weight the long side to be 100%
    def ReWeightTo100(self):
        if len(self.__Holdings):    #% if the portfolio has holdings
            wts = np.array([x.Weight for x in self.__Holdings])
            total = wts[wts>0].sum()   #% sum the positive weights only
            scalar = 100.0/total
            for i in xrange(len(self.__Holdings)):
                self.__Holdings[i].Weight *= scalar


    #% market cap is evaluated as of 'date'
    def ReWeightMarketCap(self):
        if len(self.__Holdings):   #% if the portfolio has holdings
            size = len(self.__Holdings)
            mktCaps = np.zeros(size) #% note that Weights is 1 X n
            total = 0
            for i in xrange(size):
                stk = Stock.ByWindID(self.__Holdings[i].StockID)
                mktCaps[i] = stk.FloatMarketCap(self.Date)
                if np.isnan(mktCaps[i]):
                    mktCaps[i] = 0
                total +=  mktCaps[i]
            for i in xrange(size):
                self.__Holdings[i].Weight = 100.0*mktCaps[i]/total

        # % hold the portfolio obj through "date"
        # % if reweightTo100 = true, the total long weight is 100%
        # % otherwise (default), don't reweight it
    def  HeldToDate(self, date, reweightTo100):
            if self.Date < date and len(self.__Holdings):
                size = len(self.__Holdings)
                for i in xrange(size):
                    stk = Stock.ByWindID(self.__Holdings[i].StockID)
                    ret = stk.TotalReturnInRange(self.Date, date)
                    if np.isnan(ret):
                        ret = 0
                    self.__Holdings[i].Weight = self.__Holdings[i].Weight*(1+0.01*ret)
                if reweightTo100:
                    self.ReWeightTo100()

        # % calculate total returns of the portfolio from startDate to endDate
        # % pfReturn is in percentage
    def TotalReturnInRange(self, startDate, endDate):
            startDate = Str2Date(startDate)
            endDate = Str2Date(endDate)
            pfReturn = 0
            validWt = 0
            numHoldings = len(self.__Holdings)
            for i in xrange(numHoldings):
                stk = Stock.ByWindID(self.__Holdings[i].StockID)
                stkRet = stk.TotalReturnInRange(startDate, endDate)
                if stkRet and not np.isnan(stkRet):
                    validWt = validWt + self.__Holdings[i].Weight
                    pfReturn = pfReturn + stkRet * self.__Holdings[i].Weight * 0.01
            if validWt < 95:
                print >> sys.stderr, 'less than 95% of the portfolio has valid returns'

    def GetStockIDs(self):
        return [h.StockID for h in self.__Holdings]

    @property
    def Holdings(self):
        return self.__Holdings
