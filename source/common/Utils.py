__author__ = 'xiaodan'
from datetime import datetime
import numpy

def Str2Date(date):
    '''date will be converted as a datetime obj if the date is a string,with the format "yyyymmdd" '''
    if type(date) is str:
        return datetime.strptime(date, '%Y%m%d')
    return date

def Date2Str(date):
    '''date will be converted as a datetime obj if the date is a string,with the format "yyyymmdd" '''
    if type(date) is not str:
        return date.strftime("%Y%m%d")
    return date


def WinsorizedZ(rawscores, Cap = 3.5, Tolerance = 0.1):
    ''' return a winsorized Z scores, where winsorization is robust normalization
    :param rawscores: a ndarray (numpy array) of raw scores which may include NaN
    :param Cap: the maximum Z scores
    :param Tolerance: the iteration converges when the difference of the adjacent iterations is less than Tolerance
    :return: winsorized Z scores
    '''
    n = len(rawscores)
    avg = numpy.nanmean(rawscores)
    stdev = numpy.nanstd(rawscores)
    if numpy.isnan(avg) or numpy.isnan(stdev) or numpy.isinf(avg) or numpy.isinf(stdev):
        return rawscores

    zscores = numpy.zeros(n)
    for i in range(n):
        zscores[i] = (rawscores[i]-avg)/stdev

    t = 100
    while t > Cap + Tolerance:
        avg = numpy.nanmean(zscores)
        stdev = numpy.nanstd(zscores)

        for i in range(n):
            tmpZ = (zscores[i]-avg)/stdev
            if tmpZ > Cap:
                zscores[i] = (Cap + zscores[i]) * 0.5
            elif tmpZ < -Cap:
                zscores[i] = (-Cap + zscores[i]) * 0.5
            else:
                zscores[i] = tmpZ

        max1 = abs(numpy.max(zscores))
        min1 = abs(numpy.min(zscores))
        if numpy.isnan(max1) or numpy.isnan(min1):
            return zscores
        t = max(max1, min1)

    avg = numpy.nanmean(zscores)
    stdev = numpy.nanstd(zscores)
    for i in range(n):
        zscores[i] = (zscores[i]-avg)/stdev
    return zscores


def WinsorizedZByGroup(rawscores, groups, Cap = 3.5, Tolerance = 0.1):
    ''' return a winsorized Z scores, where winsorization is robust normalization
    :param rawscores: an array of raw scores which may include NaN
    :param groups: a n by 1 array of integers which represent groups
    :param Cap: the maximum Z scores
    :param Tolerance: the iteration converges when the difference of the adjacent iterations is less than Tolerance
    :return: winsorized Z scores
    '''

    C = numpy.unique(groups)
    numGroups = len(C)
    n = len(rawscores)
    zscores = numpy.zeros(n)
    MinRequired = 3

    for i in range(numGroups):
        idx = groups == C[i]
        subrawscores = rawscores[idx]
        if len(subrawscores) < MinRequired:
            print "Warning: Not enough members in one of the groups in WinsorizedZByGroup"
            zscores[idx] = numpy.nan
        else:
            zscores[idx] = WinsorizedZ(subrawscores, Cap, Tolerance)

    return zscores