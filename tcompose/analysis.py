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
        #result = db_conn.execute("select * from news")
        result = db_conn.execute("select * from daily_prices")
        #result = db_conn.execute("select * from company_information")
        for row in result:
            print(row)
