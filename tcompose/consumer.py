#!/usr/bin/env python

import json
from kafka import KafkaConsumer
from json import dumps
from json import loads
from multiprocessing import Process
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

TOPIC_NAME = 'stock_data'
#KAFKA_SERVER = 'kafka:9092'
KAFKA_SERVER = 'kafka-1:9092'
#KAFKA_SERVER = 'kafka:9093'
#KAFKA_SERVER = 'localhost:9092'
#KAFKA_SERVER = 'localhost:9093'
#KAFKA_SERVER = '0.0.0.0:9092's
#KAFKA_SERVER= 'localhost:29092'
#consumer=KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER], value_deserializer=lambda m:loads(m.decode('utf-8')))
#now=datetime.now()
#daysago=3
#past_time=now-timedelta(days=3)
#current_time=past_time.strftime("%H:%M:00")
#current_date=past_time.strftime("%Y-%m-%d")
def stock_consumer():
    TOPIC_NAME = 'stock_data'
    # KAFKA_SERVER = 'kafka:9092'
    # KAFKA_SERVER = 'kafka:9093'
    KAFKA_SERVER = 'kafka-1:9092'
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER],value_deserializer=lambda m: loads(m.decode('utf-8')))
    for message in consumer:
        print(1)
        print(message)
        #put new data in to cold storage
        #parse the new data put it in to postgres

def news_consumer():
    TOPIC_NAME='news'
    KAFKA_SERVER = 'kafka-1:9092'
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER],value_deserializer=lambda m: loads(m.decode('utf-8')))
    for message in consumer:
        print(2)
        print(message)

"""
for message in consumer:
    #print(message[6]["Time Series (Daily)"][current_date])
    #print(message[6]["Time Series (Daily)"])
    print(message)
"""
if __name__ == '__main__':
    Process(target=stock_consumer()).start()
    Process(target=news_consumer()).start()
"""
parse the info further and put it in to storage

"""