# %% header
# % handle a time series and the related logic
# % date: 7/10/2015
import bisect
import time
import pandas as pd
import matplotlib as plt
from Utils import Str2Date

class QTimeSeries:
    def __init__(self):
        self.valueIndex = []  # vector of index of Values, mapping sorted Dates to Values
        self.dates = []  # dates on which values exist, always sorted up
        self.values = []  # cell, could be any objects, not sorted, referenced by valueIndex
        self.qseries = pd.Series(data=self.values, index=self.dates)
    # if the type of value is unknown, how to pre-allocating space for dates and values??
    # multiple scenarios:
    # 1. pass in an array of dates and values
    # 2. generate an empty timeseries with or without pre-specified
    # size of the dates
    # date is either double in the format of datenum, or char in the
    # format of 'yyyymmdd'

    def QTimeSeries(self, dates, values):
        if len(dates) != len(values):
            print 'dates has different length as values'
            return
        self.qseries = pd.Series(data=values, index=pd.to_datetime(dates).sort_index())

# % date is either double in the format of datenum, or char in the
# % format of 'yyyymmdd'

    def Add(self, date, value):
        date = Str2Date(date)
        if date not in self.qseries:
            self.qseries[date] = value
            self.qseries = self.qseries.reindex(sorted(self.qseries.index))
        else:
            self.qseries[date] = value



#         % return the value on date if the date exists
#         % otherwise return what ??
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueOn(self, date):
        date = Str2Date(date)
        if date in self.qseries:
            return self.qseries[date]
        return None


#         % return the value as of date
#         % if date < the first date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAsOf(self, date):
        date = Str2Date(date)
        return self.qseries.asof(date)
#
#         % return the value immediately after date
#         % if date > the last date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAfter(self, date):
        results = self.qseries[self.qseries > date]
        if len(results):
            return results[0]
        return None

    def Contains(self, date):
        date = Str2Date(date)
        if date in self.qseries:
            return True
        return False

    def plotTS(self, Title):
        if len(self.qseries) and isinstance(self.qseries[0], (int, long, float, complex)):
            plt.plot(self.qseries.index, self.qseries.values)
        # function plotTS(obj, Title)
        #     if (~isnumeric(obj.Values{1}))
        #         error('its value is not numeric, so it can not be ploted');
        #     else
        #         plot(obj.Dates, cell2mat(obj.Values));
        #         if (nargin>1)
        #             title(Title);
        #         end
        #         datetick('x','mm/yy');
        #     end
        # end
#
#
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'

    def Remove(self, date):
        date = Str2Date(date)
        self.qseries = self.qseries[self.qseries.index != date]

    def length(self):
        return len(self.qseries)

    def getDates(self):
        return self.qseries.index


    def FirstDate(self):
        return self.qseries.index[0]

