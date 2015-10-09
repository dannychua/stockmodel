from common.QTimeSeries import QTimeSeries
from datetime import datetime
from common.Utils import Str2Date

if __name__ == '__main__':
    # init QTimeSeries
    x = ['a', 'b', 'c'] #values
    y = [datetime(2014,2,15), datetime(2013,12,11), datetime(2015,6,13)] #dates
    pd = QTimeSeries(dates=y, values=x)


    # print Dates
    print pd.Dates

    #print firstDate
    print pd.FirstDate

    # print length
    print pd.length

    #print pandas time Series
    print pd.Series
    pd.Remove(datetime(2014,2,15))

    #print pandas time Series after removing a date
    print pd.Series
    pd.Add(datetime(2014,2,15), 'a')

    #print pandas time series after adding back
    print pd.Series

    #test contains
    print pd.Contains(datetime(2014,2,15))
    print pd.Contains(datetime(2014,2,16))

    #test ValueAfter
    print pd.ValueAfter(datetime(2014,2,15))

    #test ValueAsOf
    print pd.ValueAsOf(datetime(2014,2,16))

    #test ValueOn
    print pd.ValueOn(datetime(2014,2,15))

    print pd.Contains(Str2Date('20131211'))
    print Str2Date('20131211')