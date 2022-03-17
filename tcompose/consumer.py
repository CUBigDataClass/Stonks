#!/usr/bin/env python
from json import loads, dumps
from google.cloud import storage

from kafka import KafkaConsumer
#from google.cloud.sql.connector import connector
#import pg8000.native
#import sqlalchemy
import os

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

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='stonks-buckets.json'
bucket_name = 'stonks_chilly_storage'
destination_blob_name = 'twitter_stream'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

"""
# get pooled connection to cloud postgres instance
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)
"""
"""
print("bah")
# upload data from the stream to the bucket and postgres
for message in consumer:
    print(message)
"""

#with pool.connect() as db_conn:

for message in consumer:
    try:
        # get tweet as json
        tweet = dumps(message.value)
        print(tweet)
        # stream to the storage bucket
        blob.upload_from_string(tweet)
        #upload to postgresql
        #insert in to table for tweets
        #
    except Exception as e:
        print(e)


        # get sentiment score for the tweet
        # DO SENTIMENT ANALYSIS HERE

        # insert into postgres db
        # INSERT STATEMENT GOES HERE
