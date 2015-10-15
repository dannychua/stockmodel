__author__ = 'xiaofeng'
from nose.tools import assert_equal

from source.common.Factor import *
from source.common.Factorlib.BPCalc import *
from source.common.Utils import *


def test_GetScore():
    BP = Factor('BP','Book/Price',BPCalc)
    stkid = '601939.SH';
    date = Str2Date('20090404')
    score = BP.GetScore(stkid, date, True)   # score should be equal to 2.176
    assert_equal(round(score,3), 0.443)

test_GetScore()