__author__ = 'xiaofeng'
from nose.tools import assert_equal

from source.common.Factor import *
from source.common.Factorlib.WINDIndicators import *
from source.common.Utils import *
from source.common.PortfolioProviders import PortfolioProviders


def test_GetScore():
    BP = Factor('BP','Book/Price',BPCalc)
    stkid = '601939.SH'
    date = Str2Date('20090404')
    score = BP.GetScore(stkid, date, True)
    assert_equal(round(score,3), 0.443)

def test_Z_GetScore():
    a50PP = PortfolioProviders.getA50()
    BPFactor = Factor('BP', 'Book/Price', BPCalc, a50PP)
    BPZ = BPFactor.Z(False, a50PP)
    BPSNZ = BPFactor.Z(True, a50PP)

    stkid = '601939.SH';
    date = Str2Date('20090404')
    score = BPFactor.GetScore(stkid, date, True)
    scoreZ = BPZ.GetScore(stkid, date, True)
    scoreZSN = BPSNZ.GetScore(stkid, date, True)
    print [score, scoreZ, scoreZSN]
    assert_equal(round(score,3), 0.443)

#test_GetScore()
test_Z_GetScore()