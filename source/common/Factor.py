# %% header
# % this class is to represent a raw factor
# % Date: 8/31/2015
import sys
import os
import cPickle

import numpy as np
import pandas as pd

import Utils
from Stock import Stock
from QTimeSeries import QTimeSeries
import GlobalConstant


class Factor:
    def __init__(self, name, desc, delegator, univPP = None):
        self.Name = name
        self.Description = desc
        self.Calculator = delegator
        self.ScoreCache = None
        self.ZScoreCache = QTimeSeries()
        self.StkScoreMap = {}
        if not os.path.exists(GlobalConstant.DATA_FactorScores_DIR):
            os.mkdir(GlobalConstant.DATA_FactorScores_DIR)
        self.cacheFile = os.path.join(GlobalConstant.DATA_FactorScores_DIR, name+'.dat')
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
        elif os.path.exists(self.cacheFile):  # if cache is not available, but cache file exists, load cache from the file
            with open(self.cacheFile, 'rb') as fin:
                cacheObj = cPickle.load(fin)
                dates = [pd.to_datetime(dt, format('%Y%m%d')) for dt in cacheObj[0]]
                self.ScoreCache = QTimeSeries(dates, cacheObj[1])

            if isAsOf:
                map = self.ScoreCache.ValueAsOf(date)
            else:
                map = self.ScoreCache.ValueOn(date)
            if not map:
                print >> sys.stderr,  'date can not be found in the data cache file'
                factorScore = np.nan
            else:
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
            pf = univPP.GetPortfolioAsofFixed(dt)
            numHoldings = len(pf.Holdings)
            ids = []
            scores = [0]*numHoldings
            for i in range(numHoldings):
                score = self.Calculator(pf.Holdings[i].StockID, dt)  #%% dt doesn't need to be a trading date? strange
                scores[i] = score
                ids.append(pf.Holdings[i].StockID)
            scoreMap = dict(zip(ids, scores))
            scoreMaps.append(scoreMap)

        self.ScoreCache = QTimeSeries(dates=dates, values=scoreMaps)
        datesDT = [dt.ctime() for dt in dates]
        cacheObj = [datesDT, scoreMaps]  # cache a list instead of QTimeSeries in order to use cPickle which supports Python object only
        with open(self.cacheFile, 'wb') as fout:
            cPickle.dump(cacheObj, fout)

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
                rawscores[i] = self.GetScore(holdings[i].StockID, date, True)  ## added AsOf==True on 10/27/2015, need further tests
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
            for i in xrange(numStk):
                rawscores[i] = self.GetScore(holdings[i].StockID, date, True) ## added AsOf==True on 10/27/2015, need further tests
                sectorCode = Stock.ByWindID(holdings[i].StockID).WindSectorCode(date)
                groups[i] = sectorCode

            zscores = Utils.WinsorizedZByGroup(rawscores, groups)
            self.StkScoreMap.update(dict(zip([holding.StockID for holding in holdings], zscores)))
            self.ZScoreCache.Add(date, self.StkScoreMap)
        else:
            self.StkScoreMap = self.ZScoreCache.ValueOn(date)
        return self.StkScoreMap.get(stkID, np.nan)


    def Coverage(self, dates, isEqualWeighted = True):
        '''
        generate a time series of coverage ratios of the factor, where coverage ratio is defined as the percentage of
        stocks that have valid (non-nan) scores with either equal weights or cap weights
        :param dates: an array of dates
        :param isEqualWeighted:
        :return:
        '''
        pass


    @property
    def Name(self):
        return self.Name

    @property
    def Description(self):
        return self.Description

    @property
    def Calculator(self):
        return self.Calculator
