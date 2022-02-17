import json

from kafka import KafkaConsumer
from datetime import datetime, timedelta

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
KAFKA_SERVER = 'localhost:9092'
consumer=KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, value_deserializer=lambda m:json.loads(m.decode('utf-8')))
#now=datetime.now()
#daysago=3
#past_time=now-timedelta(days=3)
#current_time=past_time.strftime("%H:%M:00")
#current_date=past_time.strftime("%Y-%m-%d")
for message in consumer:
    #print(message[6]["Time Series (Daily)"][current_date])
    #print(message[6]["Time Series (Daily)"])
    print(message)

"""
parse the info further and put it in to storage

"""