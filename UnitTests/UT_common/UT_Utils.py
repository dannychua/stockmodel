__author__ = 'xiaofeng'
import numpy
from common.Utils import *

def UnitTests():
    a = numpy.random.normal(2, 5, 100)
    b = [a, 1000]
    b_avg = numpy.average(b)
    b_std = numpy.std(b)
    b1 = numpy.zeros(len(b))
    for i in range(len(b)):
        b1[i] = (b[i] - b_avg)/b_std

    bz = WinsorizedZ(b)
    print [b1(101), bz(101)]


if __name__ == '__main__':
    UnitTests()
    pass


        # function UnitTests()
        #     a = normrnd(2,5,100,1);
        #     b =[a;1000];
        #     b1 = (b-mean(b))/std(b);
        #     bz = Utils.WinsorizedZ(b);
        #     %[b1(101), bz(101)]
        #
        #     len = length(b);
        #     groups = zeros(len,1);
        #     for i = 1:len
        #         groups(i) = floor(i/10);
        #     end
        #     groups(len) = 1;
        #     bz2 = Utils.WinsorizedZByGroup(b, groups);
        #     [b1(1), bz(1), bz2(1)]
        #     [b1(101), bz(101), bz2(101)]
        # end