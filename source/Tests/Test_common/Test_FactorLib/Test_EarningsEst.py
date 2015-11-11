__author__ = 'xiaofeng'

from source.common.Factorlib.EarningsEst import *

stockID = '600230.SH'
date = '20140808'

fwdPE = EPFY2Calc(stockID, date)
print(fwdPE)