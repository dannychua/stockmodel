__author__ = 'xiaodan'

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_env import *


# %% header
# % store all constant variables that can be accessed globally
# % date: 9/06/2015


#test start and end date
TestStartDate = '20081231'
TestEndDate = '20141231'
DataStartDate = '20080930'

# evaluation context
# the impact of the Backtest mode has two folds:
# 1. cache mechanism: consider calculating full history in one query under the backtest mode; otherwise, calculate one date only
# 2. avoid looking ahead bais: under the debug mode, lag at least one day when taking action after the investment decision made; otherwise, use the most recent data
IsBacktest = True  # the default value is False once we move to the live trading stage
BacktestDates = None    # defined by users
BacktestCalibPP = None  # backtest calibration portfolio provider
BacktestScoringPP = None  # backtest scoring portfolio provider


#holding structure		
Holding = ['StockID', 'Weight', 'Shares', 'MarketValue']
