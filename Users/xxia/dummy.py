import numpy
from common.Factor import *
from common.Factorlib.BPCalc import *
from common.Utils import *
from common.TileAnalysis import TileAnalysis
import common.QDate as QDate
from common.PortfolioProviders import PortfolioProviders

WeekDts = QDate.WeekEndsBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
MonthDts = QDate.MonthEndsBtw(datetime.strptime('20090401', '%Y%m%d'), datetime.strptime('20141231', '%Y%m%d') )
CacheDts = QDate.UnionDistinct(WeekDts, MonthDts)
a50PP = PortfolioProviders.getA50()
BP = Factor('BP', 'Book/Price', BPCalc, a50PP)

tileAnalysis = TileAnalysis(WeekDts, a50PP, 3)
tileAnalysis.Run(BP, True)

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