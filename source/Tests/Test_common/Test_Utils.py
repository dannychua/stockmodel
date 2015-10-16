__author__ = 'xiaofeng'
from source.common.Utils import *
from nose.tools import assert_equal
from nose.tools import assert_greater

def test_Winsorization():
    a = numpy.random.normal(2, 5, 100)

    b = numpy.ma.append(a,1000)
    b_avg = numpy.nanmean(b)
    b_std = numpy.nanstd(b)
    b1 = numpy.zeros(len(b))
    for i in range(len(b)):
        b1[i] = (b[i] - b_avg)/b_std

    bz = WinsorizedZ(b)
    #print [b1[100], bz[100]]
    assert_greater(b1[100], 9)
    assert_greater(3.7, bz[100])  # the max Z is about 3.6

    # test winsorization by group
    groups = numpy.zeros(len(b))
    for i in range(len(b)):
        groups[i] = i%10

    bz2 = WinsorizedZByGroup(b, groups)
    #print [b1[0], bz[0], bz2[0]]
    #print [b1[100], bz[100], bz2[100]]
    assert_greater(bz[100], bz2[100])  # the max group-neutral-Z is smaller than winsorization-Z

test_Winsorization()
