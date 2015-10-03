import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import GlobalConstant



def BPCalc(stockID, date):
	""" Retrieve Book/Price from WINDDB """

	sqlQuery = """
       select 1/s_val_pb_new BP
       from WINDDB.DBO.AShareEODDerivativeIndicator
       where TRADE_DT='%s' and S_INFO_WINDCODE='%s'
		""" % (date, stockID)

	df = pd.read_sql(sqlQuery, GlobalConstant.DBCONN_WIND)
	bp = df.iloc[0]['BP']
	return bp