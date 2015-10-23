from source.common.Factor import *
from source.common.Utils import *
from source.common import TileAnalysis
import source.common.QDate as QDate
from source.common import PortfolioProviders
from source.common.SectorIndustry import *
from source.common.Factorlib.WINDIndicators import  *

stockID = '600230.SH'
date1 = '20140808'
date2 = '20150103'

score1 = BPCalc(stockID, date1)
print(score1)
score2 = BPCalc(stockID, date2)
print(score2)
cacheFile = GlobalConstant.DATA_FactorScores_DIR + "WindIndicatorsCache.dat"
pd.to_pickle(WindIndicatorsCache,cacheFile)



# windID = '600048.SH'
# secInd = SectorIndustry().WINDIndustry
# date = Str2Date('20140101')  # New Year Holiday
# #a = SectorIndustry.loadWINDIndustry()
#
# ts = secInd[windID]
# print ts.ValueAsOf(date)

# WeekDts = QDate.SaturdayBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
# MonthDts = QDate.MonthEndsBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
# CacheDts = QDate.UnionDistinct(WeekDts, MonthDts)
# a50PP = PortfolioProviders.getA50()
# BP = Factor('BP', 'Book/Price', BPCalc, a50PP)
#
# tileAnalysis = TileAnalysis(WeekDts, a50PP, 3)
# tileAnalysis.Run(BP, True)

# a = 5;
# print range(a)
#
# a = numpy.random.normal(2, 5, 100)
# print a.shape
# amean = numpy.nanmean(a)
# print amean
#
# b = numpy.ma.append(a,1000)
# print b.size
# print b.shape
# print b.dtype