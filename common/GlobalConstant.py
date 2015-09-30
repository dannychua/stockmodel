__author__ = 'xiaodan'
import pyodbc
from datetime import datetime
import QDate
from local_env import DBCONN_WIND
from local_env import BASE_DIR, CODE_DIR, DATA_DIR
# %% header
# % store all constant variables that can be accessed globally
# % date: 9/06/2015

#locations



#test start and end date
TestStartDate = datetime(2008, 12, 31)
TestEndDate = datetime(2014, 12, 31)
#exchange trading dates
TradingDates = QDate.GetAllTradingDays()

#holding structure
Holding = ['StockID', 'Weight', 'Shares', 'MarketValue']



