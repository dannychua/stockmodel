import numpy as np
from Stock import Stock
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
            wt = 100.0/len(self.Holdings);
            for i in xrange(len(self.Holdings)):
                self.Holdings[i].Weight = wt;

    #% re-weight the long side to be 100%
    def ReWeightTo100(self):
        if len(self.Holdings):    #% if the portfolio has holdings
            wts = np.array([x.Weight for x in self.Holdings])
            total = wts[wts>0].sum()   #% sum the positive weights only
            scalar = 100.0/total;
            for i in xrange(len(self.Holdings)):
                self.Holdings[i].Weight *= scalar


    #% market cap is evaluated as of 'date'
    def ReWeightMarketCap(self):
        if len(self.Holdings):   #% if the portfolio has holdings
            size = len(self.Holdings);
            mktCaps = np.zeros(size); #% note that Weights is 1 X n
            total = 0;
            for i in xrange(size):
                stk = Stock.ByWindID(self.Holdings[i].StockID);
                mktCaps(i) = FloatMarketCap(stk, self.Date);
                if isnan(mktCaps(i))
                    mktCaps(i) = 0;
                end
                total = total + mktCaps(i);
            end
            for i = 1:len
                self.Holdings[i].Weight = 100.0*mktCaps(i)/total;
            end
        end
    end

        % hold the portfolio obj through "date"
        % if reweightTo100 = true, the total long weight is 100%
        % otherwise (default), don't reweight it
        function HeldToDate(obj, date, reweightTo100)
            if(self.Data < daet && ~isempty(self.Holdings))
                len = length(self.Holdings);
                for i = 1:len
                    stk = Stock.ByWindID(self.Holdings[i].StockID);
                    ret = TotalReturnInRange(stk, self.Date, date);
                    if isnan(ret)
                        ret = 0;
                    end
                    self.Holdings[i].Weight = self.Holdings[i].Weight*(1+0.01*ret);
                end
                if(nargin > 2 && reweightTo100)
                    ReWeightTo100(obj);
                end
            end
        end

        % calculate total returns of the portfolio from startDate to endDate
        % pfReturn is in percentage
        function pfReturn = TotalReturnInRange(obj, startDate, endDate)
            if ischar(startDate)
                startDate = datenum(startDate, 'yyyymmdd');
            end

            if ischar(endDate)
                endDate = datenum(endDate, 'yyyymmdd');
            end

            pfReturn = 0;
            validWt = 0;
            numHoldings = length(self.Holdings);
            for i = 1:numHoldings
                stk = Stock.ByWindID(self.Holdings[i].StockID);
                stkRet = TotalReturnInRange(stk, startDate, endDate);
                if ~isnan(stkRet)
                    validWt = validWt + self.Holdings[i].Weight;
                    pfReturn = pfReturn + stkRet * self.Holdings[i].Weight * 0.01;
                end
            end
            if validWt < 95
                error('less than 95% of the portfolio has valid returns')
            end
        end

        function stockIDs = GetStockIDs(obj)
            stockIDs = char(self.Holdings.StockID);
        end

        function holdings = get.Holdings(obj)
            holdings = self.Holdings;
        end

    end

end
