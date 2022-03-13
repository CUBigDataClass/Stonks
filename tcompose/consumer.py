#!/usr/bin/env python

import json
from kafka import KafkaConsumer
from json import dumps
from json import loads
import logging
import os
import webapp2
from google.cloud import storage
from keys import *



# TOPIC_NAME = 'stock_data'
# TOPIC_NAME = 'news'
# TOPIC_NAME = 'stock'
# KAFKA_SERVER = 'kafka:9092'
KAFKA_SERVER = 'kafka-1:9092'
# KAFKA_SERVER = 'kafka:9093'
# KAFKA_SERVER = 'localhost:9092'
# KAFKA_SERVER = 'localhost:9093'
# KAFKA_SERVER = '0.0.0.0:9092's
# KAFKA_SERVER= 'localhost:29092'
# TOPIC_LIST= ['stock', 'news']
consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER], value_deserializer=lambda m: loads(m.decode('utf-8')))
consumer.subscribe('tweet')

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'stonks-bucket.json'
storage_client = storage.Client()
my_bucket= storage_client.get_bucket('stonks_chilly_storage')

"""
future ref:
creating bucket
bucket_name='w/e'
bucket=storge_client.bucket(bucket_name)
bucket.location= 'US'
bucket= storage_client.create_bucket(bucket)
"""

for message in consumer:
    # print(message[6]["Time Series (Daily)"][current_date])
    # print(message[6]["Time Series (Daily)"])
    print(message)
    try:
        bucket=
    #if (message[0]=='tweet'):
        #print("tweet")

    # print(message[0])
    # print(message[1])

# parse the info further and put it in to storage

