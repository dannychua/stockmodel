# %% header
# % handle a time series and the related logic
# % date: 7/10/2015
import pandas as pd
import matplotlib as plt
from Utils import Str2Date
from datetime import datetime

class QTimeSeries():

    def __init__(self, dates=[], values=[]):
        if len(dates) != len(values):
            print 'dates has different length as values'
            return
        if len(dates) and type(dates[0]) is str:
            dates = [Str2Date(d) for d in dates]
        self.__qSeries = pd.Series(data=values, index=dates)
        self.__qSeries = self.__qSeries.sort_index()

# % date is either double in the format of datenum, or char in the
# % format of 'yyyymmdd'

    def Add(self, date, value):
        date = Str2Date(date)
        if date not in self.__qSeries:
            self.__qSeries[date] = value
            self.__qSeries = self.__qSeries.sort_index()
        else:
            self.__qSeries[date] = value


#         % return the value on date if the date exists
#         % otherwise return what ??
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueOn(self, date):
        date = Str2Date(date)
        if date in self.__qSeries:
            return self.__qSeries[date]
        return None


#         % return the value as of date
#         % if date < the first date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAsOf(self, date):
        date = Str2Date(date)
        return self.__qSeries.asof(date)
#
#         % return the value immediately after date
#         % if date > the last date, return NaN
#         % date is either double in the format of datenum, or char in the
#         % format of 'yyyymmdd'
    def ValueAfter(self, date):
        results = self.__qSeries[self.__qSeries.index > date]
        if len(results):
            return results[0]
        return None

    def Contains(self, date):
        date = Str2Date(date)
        if date in self.__qSeries:
            return True
        return False

    def plotTS(self, Title):
        if len(self.__qSeries) and isinstance(self.__qSeries[0], (int, long, float, complex)):
            plt.plot(self.__qSeries.index, self.__qSeries.values)
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
        self.__qSeries = self.__qSeries[self.__qSeries.index != date]

    @property
    def length(self):
        return len(self.__qSeries)

    @property
    def Dates(self):
        return self.__qSeries.index

    @property
    def FirstDate(self):
        return self.__qSeries.index[0]

    @property
    def Series(self):
        return self.__qSeries



