
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
        #result = db_conn.execute("""select company_ticker from news""")
        #result = db_conn.execute("""select * from news where date_published BETWEEN '2022-04-01 01:01:00' AND '2022-04-09 01:01:01'""")
        #result = db_conn.execute("select company_ticker from companies")
        #ticker='MSFT'
        #curr_date='2021-04-10 00:00:00'
        #check = """select * from stocks where company_ticker='""" + ticker + """' AND date='""" + curr_date + """'"""
        #result= db_conn.execute(check)
        #result= db_conn.execute("""select * from stocks where company_ticker='MSFT'""")
        #result2 = db_conn.execute("select * from stocks where company_ticker='2222.SR'")
        result= db_conn.execute("""select company_ticker from stocks""")
        #result= db_conn.execute("""select * from newss where company_ticker='2222.SR' ORDER BY date DESC LIMIT 1""")
        val=0
        date1=""
        ticker="GOOG"
        #statement = """SELECT * FROM news WHERE company_ticker='""" + ticker + """' ORDER BY date_published DESC LIMIT 1"""
        #result = db_conn.execute(statement)

        for row in result:
            print(row)
            #date1=row[7]
            #print(date1)
            val+=1
        print(val)

        #date1=result.first()[0]
        #print(date1)
        #df=pd.read_sql(statement,con=db_conn)
        #df=df[df['symbol']=='AAPL']
        #print(df)
        #print (result.keys())
        #print(val)
        #print(result)


