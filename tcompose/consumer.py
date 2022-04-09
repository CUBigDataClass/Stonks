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
from sentiment import *

# this is to import from file thats in different path
import sys
loc='../../credits'
sys.path.append(loc)
from db_keys import *

# kafka configuration
TOPIC_NAME = 'tweet'
KAFKA_SERVER = 'kafka-1:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers = KAFKA_SERVER,value_deserializer = lambda m : loads(m.decode('utf-8')))
# google cloud storage configuration
"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='stonks-buckets.json'

"""

#credential reference
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'

#for bucket
bucket_name = 'stonksbucket'
destination_blob_name = 'twitter_stream'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
#currently every dataformat is in string
with pg.pool.connect() as db_conn:
    for message in consumer:
        try:
            # get tweet as json
            tweet = dumps(message.value)
            # stream to the storage bucket
            blob.upload_from_string(tweet)
            ticker=message[6]['ticker']
            url=message[6]['entities']['urls']
            content=message[6]['text']
            date=message[6]['created_at']
            followers=str(message[6]['user']['followers_count'])
            #sentimental analysis data here

            if 'extended_tweet' in message.value:
                tweet_text = message.value['extended_tweet']['full_text']
            else:
                tweet_text = message.value['text']
                # get sentiment score for the tweet

            tweet_sentiment = SentimentAnalyzer(tweet_text)
            tweet_sentiment.run_sentiment_analysis()
            sentiment_scores = tweet_sentiment.get_sentiment_score()
            # discretize compound sentiment score
            compound_sentiment = sentiment_scores['compound']
            if compound_sentiment > 0:
                # sentiment_class = 'positive'
                sentiment_class = 1
            elif compound_sentiment < 0:
                # sentiment_class = 'negative'
                sentiment_class = -1
            else:
                # sentiment_class = 'neutral'
                sentiment_class = 0
            #parse then upload to postgres tweets table
            statement = """ INSERT INTO tweets(company_ticker ,tweet_URL,tweet_content,date_published, follower_count, compound_score, sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            db_conn.execute(statement, (ticker, url, content, date, followers,compound_sentiment,sentiment_class))

        except Exception as e:
            print(e)