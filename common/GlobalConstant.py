__author__ = 'xiaodan'
import pyodbc
from datetime import datetime
import QDate
# %% header
# % store all constant variables that can be accessed globally
# % date: 9/06/2015

#locations

BASE_DIR = 'c:/ChinaA'
CODE_DIR = BASE_DIR + '/source'
DATA_DIR = BASE_DIR + '/data'

#test start and end date
TestStartDate = datetime(2008, 12, 31)
TestEndDate = datetime(2014, 12, 31)

#database connection
DBCONN_WIND = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=WindDB;UID=sa;PWD=2187')

#exchange trading dates
TradingDates = QDate.GetAllTradingDays()

#holding structure
Holding = ['StockID', 'Weight', 'Shares', 'MarketValue']



