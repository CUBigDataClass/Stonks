#!/usr/bin/env python
from json import loads, dumps
from google.cloud import storage
from kafka import KafkaConsumer
from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from postGres import *
from companies import *
# this is to import from file thats in different path
import sys
loc='../../credits'
sys.path.append(loc)
from db_keys import *

"""
def getconn() -> pg8000.native.Connection:
"""
"""
    :return: Connection to the 'stonks' db on the GCP Postgres instance
"""
"""
    conn: pg8000.native.Connection = connector.connect(
        "stonks-343022:us-central1:stock-stack",
        "pg8000",
        user="postgres",
        password="darpatliznikjuschi",
        db="stonks"
    )
    return conn
"""

# kafka configuration
TOPIC_NAME = 'tweet'
KAFKA_SERVER = 'kafka-1:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers = KAFKA_SERVER,value_deserializer = lambda m : loads(m.decode('utf-8')))
# google cloud storage configuration
"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='stonks-buckets.json'

"""

#connect to gcp postgres
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
#for postgres
pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
#for bucket
bucket_name = 'stonksbucket'
destination_blob_name = 'twitter_stream'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
#create table for tweets if not exists
#works fine but gotta convert time to date or do something idk
with pg.pool.connect() as db_conn:
    tweet = "CREATE TABLE IF NOT EXISTS tweets (tweet_ID SERIAL PRIMARY KEY, company_ticker varchar(255),tweet_URL varchar(255),tweet_content VARCHAR(255),date_published DATE, follower_count int)"
    db_conn.execute(tweet)

    for message in consumer:
        try:
            # get tweet as json
            tweet = dumps(message.value)
            # stream to the storage bucket
            blob.upload_from_string(tweet)

            #parse then upload
            statement=(
            """
            INSERT INTO tweets(company_ticker ,tweet_URL,tweet_content,date_published DATE, follower_count int)
            VALUES({},{},{},{},{}).format(message[6]['ticker'],message[6]['entities']['urls'],message[6]['text'],message[6]['created_at'],str(message[6]['user']['followers_count'])
            """)
            db_conn.execute(statement)
            #upload to postgresql
            #insert in to table for tweets
            #
        except Exception as e:
            print(e)


        # get sentiment score for the tweet
        # DO SENTIMENT ANALYSIS HERE

        # insert into postgres db
        # INSERT STATEMENT GOES HERE
