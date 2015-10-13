# Works for OS X Mavericks

import pyodbc

# FreeTDS driver
driver = '/usr/local/lib/libtdsodbc.so'

conn = pyodbc.connect(
    driver = driver,
    TDS_Version = '8.0',
    server = '192.168.1.106',
    port = 1433,
    database = 'WindDB',
    uid = 'sa',
    pwd = '12345')


stkid = '600048.SH'
dataStartDate = '20081231'
dataEndDate = '20150110'
sqlString = """select TRADE_DT, S_DQ_ADJCLOSE from WindDB.dbo.ASHAREEODPRICES  where S_INFO_WINDCODE ='%s' order by trade_dt""" %stkid
cursor = conn.cursor()
cursor.execute(sqlString)
for date, price in cursor.fetchall():
    print date, price