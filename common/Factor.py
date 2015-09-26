# %% header
# % this class is to represent a raw factor
# % Date: 8/31/2015
import sys
import os
import cPickle
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
            portfolio = GetPortfolioAsofFixed(univPP, dt)
            numHoldings = len(portfolio.Holdings)
            ids = cell(1, numHoldings)
            scores = zeros(1, numHoldings)
            for j = 1:numHoldings
                score = obj.Calculator(portfolio.Holdings(j).StockID, dt)  %% dt doesn't need to be a trading date? strange
                %disp([j,size(score)])
                scores(j) = score
                ids{j} = portfolio.Holdings(j).StockID
            end
            scoreMap = containers.Map(ids, scores)
            Add(cache, dt, scoreMap)
        end
        obj.ScoreCache = cache
        save(obj.cacheFile, 'cache')
    end
#
#         % transform a raw factor to a Z factor
#         function zFactor = Z(obj, isSectorNeutral, universe)
#             univ = []
#             if(nargin > 2)
#                 univ = universe
#             elseif (~isempty(obj.UnivPP))
#                 univ = obj.UnivPP
#             else
#                 error('No universe is defined')
#             end
#
#             zScoreCache = QTimeSeries()
#             stkScoreMap = []
#             % inner function to calculate Z scores from raw scores
#             function score = zCalc(stkID, date)
#                 if (~Contains(zScoreCache, date))
#                     portfolio = GetPortfolioAsofFixed(universe, date)
#                     if(isempty(portfolio))
#                         error(['No Portfolio can be found on ', datestr(date,'yyyymmdd')])
#                     end
#
#                     holdings = portfolio.Holdings
#                     numStk = length(holdings)
#                     rawscores = zeros(numStk,1)
#                     for i=1:numStk
#                         stkID = holdings(i).StockID
#                         rawscores(i) = GetScore(obj, stkID, date)
#                     end
#                     zscores = Utils.WinsorizedZ(rawscores)
#                     for i=1:numStk
#                         stkID = holdings(i).StockID
#                         stkScoreMap = [stkScoreMap containers.Map(stkID, zscores(i))]
#                     end
#                     Add(zScoreCache, date, stkScoreMap)
#                 else
#                     stkScoreMap = ValueOn(zScoreCache, date)
#                 end
#
#                 if(isKey(stkScoreMap, stkID))
#                     score = stkScoreMap(stkID)
#                 else
#                     score = nan
#                 end
#             end
#
#             % inner function to calculate sector-neutral Z scores from raw scores
#             function score = zCalc_SN(stkID, date)
#                 if (~Contains(zScoreCache, date))
#                     portfolio = GetPortfolioAsofFixed(universe, date)
#                     if(isempty(portfolio))
#                         error(['No Portfolio can be found on ', datestr(date,'yyyymmdd')])
#                     end
#
#                     holdings = portfolio.Holdings
#                     numStk = length(holdings)
#                     rawscores = zeros(numStk,1)
#                     groups = cell(numStk,1)
#                     groupIdx = 1
#                     for i=1:numStk
#                         stkID = holdings(i).StockID
#                         rawscores(i) = GetScore(obj, stkID, date)
#                         sectorCode = WindSectorCode(Stock.ByWindID(stkID), date)
#                         groups(i) = {sectorCode}
#                     end
#                     %groups = char(groups)
#                     [C, ia, groupIdx] = unique(groups)
#                     zscores = Utils.WinsorizedZByGroup(rawscores, groupIdx)
#                     for i=1:numStk
#                         stkID = holdings(i).StockID
#                         stkScoreMap = [stkScoreMap containers.Map(stkID, zscores(i))]
#                     end
#                     Add(zScoreCache, date, stkScoreMap)
#                 else
#                     stkScoreMap = ValueOn(zScoreCache, date)
#                 end
#
#                 if(isKey(stkScoreMap, stkID))
#                     score = stkScoreMap(stkID)
#                 else
#                     score = nan
#                 end
#             end
#
#             name = [obj.Name, '_Z']
#             desc = [obj.Description, '_Z']
#             if(isSectorNeutral)
#                 name = [name, '_SN']
#                 desc = [desc, '_SN']
#                 zFactor = Factor(name, desc, @zCalc_SN, universe)
#             else
#                 zFactor = Factor(name, desc, @zCalc, universe)
#             end
#         end
#
#         function name = get.Name(obj)
#             name = obj.Name
#         end
#
#         function desc = get.Description(obj)
#             desc = obj.Description
#         end
#
#         function calc = get.Calculator(obj)
#             calc = obj.Calculator
#         end
#     end
# end