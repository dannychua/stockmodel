__author__ = 'xiaofeng'
import numpy
from common.Utils import *

def UnitTests():
    a = numpy.random.normal(2, 5, 100)
    b = numpy.ma.append(a,1000)
    b_avg = numpy.nanmean(b)
    b_std = numpy.nanstd(b)
    b1 = numpy.zeros(len(b))
    for i in range(len(b)):
        b1[i] = (b[i] - b_avg)/b_std

    bz = WinsorizedZ(b)
    print [b1[100], bz[100]]

    groups = numpy.zeros(len(b))
    for i in range(len(b)):
        groups[i] = i%10

    bz2 = WinsorizedZByGroup(b, groups)
    print [b1[0], bz[0], bz2[0]]
    print [b1[100], bz[100], bz2[100]]

if __name__ == '__main__':
    UnitTests()
    pass
