__author__ = 'xiaodan'
import time

def checkDate(date):
    if type(date) is str:
        return time.strptime(date, '%Y%m%d')
    return date