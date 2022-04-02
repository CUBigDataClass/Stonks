#!/usr/bin/env python
from json import loads, dumps
from google.cloud import storage
from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from postGres import *

from companies import *
from dailystock import *
# this is to import from file thats in different path
from db_keys import *


#connect to gcp postgres
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
#for postgres
pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
st=stocks(pg)
#for bucket

#print(st.get_prices_df_query())
with pg.pool.connect() as db_conn:
    # drop table to avoid making two tables
    command="DROP TABLE IF EXISTS tweets"
    db_conn.execute(command)
    command="DROP TABLE IF EXISTS news"
    db_conn.execute(command)
    #command = "DROP TABLE IF EXISTS daily_prices"
    #db_conn.execute(command)
    #command = "DROP TABLE IF EXISTS company_informatiosn"
    #db_conn.execute(command)
    tweet = "CREATE TABLE IF NOT EXISTS tweets (tweet_ID SERIAL PRIMARY KEY, company_ticker varchar(255),tweet_URL varchar(255),tweet_content VARCHAR(300),date_published DATE, follower_count int, sentiment float)"
    db_conn.execute(tweet)
    news = "CREATE TABLE IF NOT EXISTS news (article_id SERIAL PRIMARY KEY, company_ticker varchar(255), title varchar(255), author varchar(255), article_URL VARCHAR(255), url_image VARCHAR(255),article_description VARCHAR(10000), date_published timestamp)"
    db_conn.execute(news)
#populates companies table in postgres and companies blob in bucket
#st.get_top_companies_info()
#create prices table
#input all the historical prices
st.create_all_prices_table()
st.insert_all_historical_prices()

