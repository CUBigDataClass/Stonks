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
from all_articles_bloomberg import *

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
    """
    command="DROP TABLE IF EXISTS companies"
    db_conn.execute(command)
    command="DROP TABLE IF EXISTS tweets"
    db_conn.execute(command)
    """
    command="DROP TABLE IF EXISTS news"
    db_conn.execute(command)
    command="DROP TABLE IF EXISTS stocks"
    db_conn.execute(command)
    """
    company = "CREATE TABLE IF NOT EXISTS companies (company_ticker varchar(255) PRIMARY KEY,company_name varchar(255), sector varchar(255), exchange varchar(255), website varchar(255))"
    db_conn.execute(company)
    tweet = "CREATE TABLE IF NOT EXISTS tweets (tweet_ID SERIAL PRIMARY KEY, company_ticker varchar(255),tweet_URL text[],tweet_content VARCHAR(5000),date_published timestamp, follower_count int, compound_score float, sentiment int)"
    db_conn.execute(tweet)
    """
    stocks = "CREATE TABLE IF NOT EXISTS stocks (date timestamp, company_ticker varchar(255),open numeric,high numeric,low numeric, close numeric, volume numeric, dividends numeric, PRIMARY KEY(company_ticker,date))"
    db_conn.execute(stocks)
    news = "CREATE TABLE IF NOT EXISTS news (article_id SERIAL PRIMARY KEY, company_ticker varchar(255), title varchar(255), author varchar(255), article_URL VARCHAR(255), url_image VARCHAR(255),article_description VARCHAR(10000), date_published timestamp)"
    db_conn.execute(news)

#populates companies table in postgres and companies blob in bucket
#st.get_top_companies_info()
#create prices table
#input all the historical prices
#st.insert_all_historical_prices()
#st.insert_all_latest_stock_data()
#st.get_top_companies_info()
#st.insert_all_historical_prices()
#newsArticles = NewsArticles(API_KEY_NEWSAPI,top100,SOURCES,LANGUAGES)
#newsArticles.get_everything()


