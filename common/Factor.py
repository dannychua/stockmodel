# %% header
# % this class is to represent a raw factor
# % Date: 8/31/2015
import sys
import os
import cPickle
import numpy as np
import Utils
from Stock import Stock
from datetime import datetime
from QTimeSeries import QTimeSeries
import GlobalConstant


class Factor:
    def __init__(self, name, desc, delegator, univPP):
        self.Name = name
        self.Description = desc
        self.Calculator = delegator
        self.ScoreCache = None
        self.ZScoreCache = QTimeSeries()
        self.StkScoreMap = {}
        if not os.path.exists(GlobalConstant.DATA_DIR+'/FactorScores/'):
            os.mkdir(GlobalConstant.DATA_DIR+'/FactorScores/')
        self.cacheFile = GlobalConstant.DATA_DIR+'/FactorScores/' + name+'.mat'
        self.UnivPP = univPP
        
        # get the score from the cache if it is available
        # otherwise calculate it on the fly
        # if the cache exists, but the date or the stock doesn't not,
        # return NaN
        # call self.Calculator directly if calculating on the fly

    def GetScore(self, stockID, date, isAsOf=False):
        # % ValueOn or AsOf depending on the parameter, the default is ValueOn
        if self.ScoreCache: #load from cache if it is available
            # ValueOn or AsOf depending on the parameter, the default is ValueOn
            # load from cache if it is available
            if isAsOf:
                map = self.ScoreCache.ValueAsOf(date)
            else:
                map = self.ScoreCache.ValueOn(date)
            if not map:
                print >> sys.stderr,  'date can not be found in the data cache'
                factorScore = np.nan
            else:
                factorScore = map[stockID]
        elif os.exits(self.cacheFile):  # if cache is not available, but cache file exists, load cache from the file
            self.ScoreCache = cPickle.load(self.cacheFile)
            if isAsOf:
                map = self.ScoreCache.ValueAsOf(date)
            else:
                map = self.ScoreCache.ValueOn(date)
            factorScore = map[stockID]
        else:
            factorScore = self.Calculator(stockID,date) #% calculate on the fly
        return factorScore
#
#         % calculate the factor scores once and save it to the cache file
#         % dates is a vector of Matlab dates on which the scores are calculated and saved
#         % univPP is a universe PortfolioProvider
    def CalcScoresAndSave(self, dates, univPP):
        scoreMaps = []
        for idx, dt in enumerate(dates):
            port = univPP.GetPortfolioAsofFixed(dt)
            ids = []
            scores = []
            for holding in port.Holdings:
                score = self.Calculator(holding.StockID, dt.strftime('%Y%m%d'))  #%% dt doesn't need to be a trading date? strange
                #%disp([j,size(score)])
                scores.append(score)
                ids.append(holding.StockID)
            scoreMap = dict(zip(ids, scores))
            scoreMaps.append(scoreMap)
        self.ScoreCache = QTimeSeries(dates=dates, values=scoreMaps)
        with open(self.cacheFile, 'w') as fout:
            cPickle.dump(self.ScoreCache, fout)

#
#         % transform a raw factor to a Z factor
        #needs to be rewritten
    def Z(self, isSectorNeutral, universe=None):
        if universe:
            univ = universe
        elif len(self.UnivPP):
            univ = self.UnivPP
        else:
            print >> sys.stderr, 'No universe is defined'
            return
            self.ZScoreCache = QTimeSeries()
            self.StkScoreMap = {}
        name = self.Name + '_Z'
        desc = self.Description + '_Z'
        if isSectorNeutral:
            name += '_SN'
            desc += '_SN'
            return Factor(name, desc, self.zCalc_SN, univ)
        else:
            return Factor(name, desc, self.zCalc, univ)

    # % inner function to calculate Z scores from raw scores
    def zCalc(self, stkID, date):
        date = Utils.Str2Date(date)
        if date not in self.ZScoreCache.Dates:
            portfolio = self.UnivPP.GetPortfolioAsofFixed(date)
            if not portfolio:
                print >> sys.stderr, 'No Portfolio can be found on ', str(date)
                return np.nan
            holdings = portfolio.Holdings
            numStk = len(holdings)
            rawscores = np.zeros(numStk)
            for i in xrange(numStk):
                rawscores[i] = self.GetScore(holdings[i].StockID, date)
            zscores = Utils.WinsorizedZ(rawscores)
            self.StkScoreMap.update(dict(zip([holding.StockID for holding in holdings], zscores)))
            self.ZScoreCache.Add(date, self.StkScoreMap)
        else:
            self.StkScoreMap = self.ZScoreCache.ValueOn(date)

        return self.StkScoreMap.get(stkID, np.nan)


        #% inner function to calculate sector-neutral Z scores from raw scores
    def zCalc_SN(self, stkID, date):
        date = Utils.Str2Date(date)
        if date not in self.ZScoreCache.Dates:
            portfolio = self.UnivPP.GetPortfolioAsofFixed(date)
            if not portfolio:
                print >> sys.stderr, 'No Portfolio can be found on ', str(date)
                return np.nan
            holdings = portfolio.Holdings
            numStk = len(holdings)
            rawscores = np.zeros(numStk)
            groups = np.arange(numStk)
            groupIdx = 1
            for i in xrange(numStk):
                rawscores[i] = self.GetScore(holdings[i].StockID, date)
                sectorCode = Stock.ByWindID(holdings[i].StockID).WindSectorCode(date)
                groups[i] = sectorCode

                #%groups = char(groups)
            #[C, ia, groupIdx] = unique(groups)
            zscores = Utils.WinsorizedZByGroup(rawscores, groupIdx)
            self.StkScoreMap.update(dict(zip([holding.StockID for holding in holdings], zscores)))
        else:
            self.StkScoreMap = self.ZScoreCache.ValueOn(date)
        return self.StkScoreMap.get(stkID, np.nan)

    @property
    def Name(self):
        return self.Name

    @property
    def Description(self):
        return self.Description

    @property
    def Calculator(self):
        return self.Calculator
