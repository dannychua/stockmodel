import pyodbc


# Directories
BASE_DIR = '.'
CODE_DIR = BASE_DIR + '/source'
DATA_DIR = BASE_DIR + '/data'


# Database connection
driver = '/usr/local/lib/libtdsodbc.so'    # FreeTDS driver
DBCONN_WIND  = pyodbc.connect(
    driver = driver,
    TDS_Version = '8.0',
    server = '192.168.1.106',
    port = 1433,
    database = 'WindDB',
    uid = 'sa',
    pwd = '12345')
