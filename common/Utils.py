__author__ = 'xiaodan'
import time

# date will be converted as a datetime obj if the date is a string,
def checkDate(date):
    if type(date) is str:
        return time.strptime(date, '%Y%m%d')
    return date