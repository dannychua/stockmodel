__author__ = 'xiaodan'
import pyodbc
# initialize the environment variables
# date: 8/31/2015

# test variables

stkid = '600048.SH'
dataStartDate = '20081231';
dataEndDate = '20150110';
sqlString = """select TRADE_DT, S_DQ_ADJCLOSE from WindDB.dbo.ASHAREEODPRICES  where S_INFO_WINDCODE ='%s' order by trade_dt""" %stkid


cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=WindDB;UID=sa;PWD=2187')
cursor = cnxn.cursor()
cursor.execute(sqlString)
for date, price in cursor.fetchall():
    print date, price