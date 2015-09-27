__author__ = 'xiaofeng'

import pyodbc

stkid = '600048.SH'
dataStartDate = '20141231'
dataEndDate = '20150110'
sqlString = """select TRADE_DT, S_DQ_ADJCLOSE from WindDB.dbo.ASHAREEODPRICES  where S_INFO_WINDCODE ='%s' order by trade_dt""" %stkid

#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=WindDB;UID=sa;PWD=YOURPASSWORD')
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=WindDB')
cursor = cnxn.cursor()
cursor.execute(sqlString)
for date, price in cursor.fetchall():
   print date, price

