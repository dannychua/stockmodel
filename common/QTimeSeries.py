# %% header
# % handle a time series and the related logic
# % date: 7/10/2015
import pandas as pd
import matplotlib as plt
from Utils import Str2Date


class QTimeSeries():
    def __init__(self, dates=[], values=[]):
        if len(dates) != len(values):
            print 'dates has different length as values'
            print len(dates)
            print len(values)
            return
        self._QTimeSeries__valueDict = {}
        if len(dates) and type(dates[0]) is str:
            dates = [Str2Date(d) for d in dates]
        for idx, value in enumerate(values):
            self._QTimeSeries__valueDict[idx] = value
        if not len(dates):
            self._QTimeSeries__qSeries = pd.Series()
        else:
            self._QTimeSeries__qSeries = pd.Series(data=xrange(len(values)), index=dates)
            self._QTimeSeries__qSeries = self._QTimeSeries__qSeries.sort_index()


# % date is either double in the format of datenum, or char in the
# % format of 'yyyymmdd'

    def Add(self, date, value):
        date = Str2Date(date)
        if date not in self._QTimeSeries__qSeries:
            loc = len(self._QTimeSeries__valueDict)
            self._QTimeSeries__qSeries[date] = loc
            self._QTimeSeries__valueDict[loc] = value
            self._QTimeSeries__qSeries = self._QTimeSeries__qSeries.sort_index()
        else:
            loc = self._QTimeSeries__qSeries[date]
            self.__valueDict[loc] = value
        return loc


#         % return the value on date if the date exists
#         % otherwise return what ??
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueOn(self, date):
        date = Str2Date(date)
        if date in self._QTimeSeries__qSeries:
            return self._QTimeSeries__valueDict[self._QTimeSeries__qSeries[date]]
        return None


#         % return the value as of date
#         % if date < the first date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAsOf(self, date):
        date = Str2Date(date)
        if len(self._QTimeSeries__qSeries):
            return self._QTimeSeries__valueDict[self._QTimeSeries__qSeries.asof(date)]
        return None
#
#         % return the value immediately after date
#         % if date > the last date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAfter(self, date):
        results = self._QTimeSeries__qSeries[self._QTimeSeries__qSeries.index > date]
        if len(results):
            return self._QTimeSeries__valueDict[results[0]]
        return None

    def Contains(self, date):
        date = Str2Date(date)
        if date in self._QTimeSeries__qSeries:
            return True
        return False

    def plotTS(self, Title):
        if len(self._QTimeSeries__qSeries) and isinstance(self._QTimeSeries__qSeries[0], (int, long, float, complex)):
            plt.plot(self._QTimeSeries__qSeries.index, self._QTimeSeries__qSeries.values)
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
        self._QTimeSeries__qSeries = self._QTimeSeries__qSeries[self._QTimeSeries__qSeries.index != date]

    @property
    def length(self):
        return len(self._QTimeSeries__qSeries)

    @property
    def Dates(self):
        return self._QTimeSeries__qSeries.index

    @property
    def FirstDate(self):
        return self._QTimeSeries__qSeries.index[0]

    @property
    def Series(self):
        return self._QTimeSeries__qSeries, self._QTimeSeries__valueDict

    @property
    def Timeseries(self):
        # Create timeseries from qSeries and valueDict
        # Warning: No error handling. A temp convenience function for Danny until code rewrite
        # TODO: Exception handling
        qSeries, valueDict = self.Series
        timeseries = qSeries.copy()
        for index, row in qSeries.iteritems():
            timeseries.loc[index] = valueDict[row]    # variable 'row' is an reference index for valueDict
        return timeseries
