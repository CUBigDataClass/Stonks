#!/usr/bin/env python

import json
from kafka import KafkaConsumer
from json import dumps
from json import loads

from keys import *


"""
To DO:
find out db structure
    how we saving information
    paths, details
problems: might need better api 
    alphadvantage only gives from 3days ago
    if we are using GCP figure out what port to use for kafka_server
    possible candidates yahoofinance, google finance.
    could we possibly pull historical data from alphadvantage and pull more real time from yahoo/google?

"""

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
# consumer.subscribe(TOPIC_NAME)
consumer.subscribe(['stock', 'news'])


for message in consumer:
    # print(message[6]["Time Series (Daily)"][current_date])
    # print(message[6]["Time Series (Daily)"])
    print(message)
    if (message[0] == 'stock'):
        print("russia")
    elif (message[0] == 'news'):
        print("news")

    # print(message[0])
    # print(message[1])

# parse the info further and put it in to storage

