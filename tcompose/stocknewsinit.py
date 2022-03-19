import pg8000.native
import sqlalchemy
import yfinance as yf
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from postGres import *
from companies import *
import sys
sys.path.append('C:/Users/13038/Desktop')
from db_keys import *
from dailystock import *

# run this file once
if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../creds.json'
    pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
    st = stocks(pg)
    st.get_top_companies_info()
    # print(st.get_prices_df_query())
    st.create_all_prices_table()
    #print(st.get_prices_df_query())
    st.insert_all_historical_prices()
    #print(st.get_prices_df_query())
    news = "CREATE TABLE IF NOT EXISTS news (article_id SERIAL PRIMARY KEY, company_ticker varchayhhr(255), article_URL VARCHAR(255), article_content VARCHAR(255)"

