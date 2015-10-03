# %% header
# % this class is to represent a raw factor
# % Date: 8/31/2015
import sys
import os
import cPickle
import numpy as np
import Utils
from Stock import Stock
from QTimeSeries import QTimeSeries

class Factor:
    def __init__(self, name, desc, delegator, univPP):
        self.name = name
        self.description = desc
        self.calculator = delegator
        self.cacheFile = None # obj.cacheFile = fullfile(GlobalConstant.DATA_DIR, ['FactorScores\', obj.Name, '.mat'])
        self.univPP = univPP
        
        # get the score from the cache if it is available
        # otherwise calculate it on the fly
        # if the cache exists, but the date or the stock doesn't not,
        # return NaN
        # call self.calculator directly if calculating on the fly

    def getScore(self, stockID, date, isAsOf=False):
        # % ValueOn or AsOf depending on the parameter, the default is ValueOn
        if not self.scoreCache: #load from cache if it is available
            # ValueOn or AsOf depending on the parameter, the default is ValueOn
            if len(self.ScoreCache):   # load from cache if it is available
                if isAsOf:
                    map = self.ScoreCache.ValueAsOf(date)
                else:
                    map = self.scoreCache.ValueOn(date)
                if not map:
                    print >> sys.stderr,  'date can not be found in the data cache'
                    return
                factorScore = map[stockID]
            elif os.exits(self.cacheFile):  # if cache is not available, but cache file exists, load cache from the file
                self.ScoreCache = cPickle.load(self.cacheFile)
                if isAsOf:
                    map = self.ScoreCache.ValueAsOf(date)
                else:
                    map = self.scoreCache.ValueOn(date)
                factorScore = map[stockID]
            else:
                factorScore = self.Calculator(stockID,date) #% calculate on the fly
        return factorScore
#
#         % calculate the factor scores once and save it to the cache file
#         % dates is a vector of Matlab dates on which the scores are calculated and saved
#         % univPP is a universe PortfolioProvider
    def CalcScoresAndSave(self, dates, univPP):
        datesLen = len(dates)
        cache = QTimeSeries()
        for i in xrange(datesLen):
            dt = dates[i]
            #%disp(datestr(dt,'yyyymmdd'))
            #%portfolio = GetPortfolioOn(univPP, dt)
            portfolio = univPP.GetPortfolioAsofFixed(dt)
            numHoldings = len(portfolio.Holdings)
            ids = np.arange(numHoldings)
            scores = np.zeros(numHoldings)
            for j in xrange(numHoldings):
                score = self.Calculator(portfolio.Holdings[j].StockID, dt)  #%% dt doesn't need to be a trading date? strange
                #%disp([j,size(score)])
                scores[j] = score
                ids [j] = portfolio.Holdings[j].StockID
            scoreMap = dict(zip(ids, scores))
            cache.Add(dt, scoreMap)
        self.ScoreCache = cache
        with open(self.cacheFile, 'w') as fout:
            cPickle.dump(cache, fout)

#
#         % transform a raw factor to a Z factor
        #needs to be rewritten
    def Z(self, isSectorNeutral, universe=None):
        univ = []
        if universe:
            univ = universe
        elif len(self.UnivPP):
            univ = self.UnivPP
        else:
            print >> sys.stderr, 'No universe is defined'
            return
            zScoreCache = QTimeSeries()
            stkScoreMap = {}
        name = self.name + '_Z'
        desc = self.description + '_Z'
        if isSectorNeutral:
            name += '_SN'
            desc += '_SN'
            return Factor(name, desc, zCalc_SN, universe)
        else:
            return Factor(name, desc, zCalc, universe)

    # % inner function to calculate Z scores from raw scores
    def zCalc(self, stkID, date, universe, zScoreCache, stkScoreMap):
        if date not in zScoreCache:
            portfolio = universe.GetPortfolioAsofFixed(date)
            if not len(portfolio):
                print >> sys.stderr, 'No Portfolio can be found on ', str(date)
                return
            holdings = portfolio.Holdings
            numStk = len(holdings)
            rawscores = np.zeros(numStk)
            for i in xrange(numStk):
                rawscores[i] = self.GetScore(holdings[i].StockID, date)
            zscores = Utils.WinsorizedZ(rawscores)
            stkScoreMap.update(dict(zip([holding.stdID for holding in holdings], zscores)))
            zScoreCache.Add(date, stkScoreMap)
        else:
            stkScoreMap = zScoreCache.ValueOn(date)

        return stkScoreMap.get(stkID, np.nan)


        #% inner function to calculate sector-neutral Z scores from raw scores
    def zCalc_SN(self, stkID, date, universe, zScoreCache, stkScoreMap, isSectorNeutral):
        if date not in zScoreCache:
            portfolio = universe.GetPortfolioAsofFixed(date)
            if not len(portfolio):
                print >> sys.stderr, 'No Portfolio can be found on ', str(date)
                return
            holdings = portfolio.Holdings
            numStk = len(holdings)
            rawscores = np.zeros(numStk)
            groups = np.arange(numStk)
            groupIdx = 1
            for i in xrange(numStk):
                stkID = holdings[i].StockID
                rawscores[i] = self.GetScore(stkID, date)
                sectorCode = Stock.ByWindID(stkID).WindSectorCode(date)
                groups[i] = sectorCode

                #%groups = char(groups)
            #[C, ia, groupIdx] = unique(groups)
            zscores = Utils.WinsorizedZByGroup(rawscores, groupIdx)
            stkScoreMap.update(dict(zip([holding.stdID for holding in holdings], zscores)))
        else:
            zScoreCache.ValueOn(date)
        return stkScoreMap.get(stkID, np.nan)


    def getName(self):
        return self.Name

    def getDescription(self):
        return self.Description

    def getCalculator(self):
        return self.Calculator
