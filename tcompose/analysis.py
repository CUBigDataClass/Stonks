from request_parameters import *
# from keys import *

from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
import yfinance as yf
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from google.cloud import storage
from postGres import *
from companies import *
from dailystock import *
from datetime import *


#this is to check if everything in the postgresql db was working properly
#query and print each table

if __name__ == "__main__":
    credential_path='creds.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
    st=stocks(pg)
    #st.query_company_information()
    #st.query_daily_prices()
    with pg.pool.connect() as db_conn:
        #result = db_conn.execute("select * from tweets")
        #result = db_conn.execute("select date_published from news")
        #result = db_conn.execute("""select * from news where date_published BETWEEN '2016-06-22 19:10:25' AND '2022-01-01 01:01:01'""")
        #result = db_conn.execute("select 'daily_prices.Low' From daily_prices")
        #result = db_conn.execute("select 'Company_Symbol' from company_information")
        #statement= "select * from daily_prices"
        for row in result:
            print(row)
        #df=pd.read_sql(statement,con=db_conn)
        #df=df[df['symbol']=='AAPL']
        #print(df)
        #print (result.keys())
        #print(result)

