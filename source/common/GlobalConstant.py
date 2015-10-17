__author__ = 'xiaodan'

from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_env import *


# %% header
# % store all constant variables that can be accessed globally
# % date: 9/06/2015


#test start and end date
TestStartDate = datetime(2008, 12, 31)
TestEndDate = datetime(2014, 12, 31)

#holding structure		
Holding = ['StockID', 'Weight', 'Shares', 'MarketValue']
