import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import wget
import os
from sqlalchemy import create_engine
import psycopg2

import os

cwd = os.getcwd()
sqlfilename = cwd + '/createsensortable.sql'
f = open(sqlfilename, "r")
fs = f.read()

engine = create_engine('postgresql://pythonuser:pythonuser@localhost:5432/data')

connection = engine.raw_connection()
try:
    cursor = connection.cursor()
    cursor.execute(fs)
finally:
    connection.commit()
    connection.close()

sqlcmnd = "INSERT INTO public.raw_sensordata(index, millitime, band, value) VALUES (1, 2, 3, 4)";
    
#sqlcmnd = 'COPY "raw_CovidTrackerGantt" FROM \''+ filename + '\' DELIMITER \',\' CSV;'
with engine.connect().execution_options(autocommit=True) as con:
  con.execute(sqlcmnd)

