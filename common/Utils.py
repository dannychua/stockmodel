__author__ = 'xiaodan'
import time
import numpy

def Str2Date(date):
    '''date will be converted as a datetime obj if the date is a string,with the format "yyyymmdd" '''
    if type(date) is str:
        return time.strptime(date, '%Y%m%d')
    return date

def WinsorizedZ(rawscores, Cap = 3.5, Tolerance = 0.1):
    ''' return a winsorized Z scores, where winsorization is robust normalization
    :param rawscores: an array of raw scores which may include NaN
    :param Cap: the maximum Z scores
    :param Tolerance: the iteration converges when the difference of the adjacent iterations is less than Tolerance
    :return: winsorized Z scores
    '''
    n = len(rawscores)
    avg = numpy.average(rawscores)   ## can it handle NaN?
    stdev = numpy.std(rawscores)     ## is it simple sample standard deviation? does it handle NaN?
    pass

        # function zscores = WinsorizedZ(rawscores, cap, tolerance)
        #     Cap = 3.5;
        #     Tolerance = 0.1;
        #     if(nargin>1)
        #         Cap = cap;
        #         if(nargin >2)
        #             Tolerance = tolerance;
        #         end
        #     end
        #
        #     len = length(rawscores);
        #     zscores = zeros(len,1);
        #
        #     avg = nanmean(rawscores);
        #     stdev = nanstd(rawscores);
        #
        #     if(isnan(avg) || isnan(stdev) || isinf(avg) || isinf(stdev))
        #         zscores = rawscores;
        #         return;
        #     end
        #
        #     zscores = (rawscores-avg)/stdev;
        #
        #     t = 100;
        #     while (t > Cap +Tolerance)
        #         avg = nanmean(zscores);
        #         stdev = nanstd(zscores);
        #
        #         tmpZ = (zscores-avg)/stdev;
        #
        #         for i = 1:len
        #             if(tmpZ(i) > Cap)
        #                 zscores(i) = (Cap+zscores(i))*0.5;
        #             elseif (tmpZ(i) < -Cap)
        #                 zscores(i) = (-Cap+zscores(i))*0.5;
        #             else
        #                 zscores(i) = tmpZ(i);
        #             end
        #         end
        #
        #         max1 = abs(nanmax(zscores));
        #         min1 = abs(nanmin(zscores));
        #         if(isnan(max1) || isnan(min1))
        #             return;
        #         end
        #         t = max(max1, min1);
        #     end
        #
        #     avg = nanmean(zscores);
        #     stdev = nanstd(zscores);
        #     zscores = (zscores-avg)/stdev;
        # end
        #


