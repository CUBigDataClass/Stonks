#from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
import yfinance as yf
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from postGres import *
from companies import *

# this is to import from file thats in different path
import sys
loc='C:/Users/13038/Desktop'
sys.path.append(loc)
from db_keys import *

# run this file once
#creates table
if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../creds.json'
    pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
    with pg.pool.connect() as db_conn:
        tweet="CREATE TABLE IF NOT EXISTS tweets (tweet_ID SERIAL PRIMARY KEY, company_ticker varchar(255),tweet_URL varchar(255),tweet_content VARCHAR(255),date_published VARCHAR(255), follower_count int"
        news="CREATE TABLE IF NOT EXISTS news (article_id SERIAL PRIMARY KEY, company_ticker varchayhhr(255), article_URL VARCHAR(255), article_content VARCHAR(255)"
        db_conn.execute(tweet)
        db_conn.execute(news)

