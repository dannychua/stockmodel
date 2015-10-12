import pyodbc
#database connection
BASE_DIR = 'c:/ChinaA'
CODE_DIR = BASE_DIR + '/source'
DATA_DIR = BASE_DIR + '/data'
DATA_FactorScores_DIR = BASE_DIR + '/data/FactorScores'
DBCONN_WIND = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=WindDB;UID=sa;PWD=2187')