#!/usr/bin/env python
from tweepy import Stream
import json
from keys import *
#from companies import *
from kafka import KafkaProducer
import sys



class TwitterStream(Stream):
    """
    Inherits from tweepy's Stream class. We are only modifying the few functions
    we need to customize, namely what to do when new tweets come through.
    """

    def get_companies(self, tweet):
        """
        :param tweet: The string text of a tweet.
        :return: A list of companies mentioned in the tweet.
        """
        tweet = tweet.lower()
        companies_mentioned = []
        for stock in top100:
            if stock in tweet:
                companies_mentioned.append(stock)

        return companies_mentioned

    def on_data(self, raw_data):
        """
        Gets called every time a new tweet gets filtered through.
        """
        self.process_data(raw_data)

        return True

    def process_data(self, raw_data):
        """
        Sends data through the Kafka log.
        """
        response = json.loads(raw_data)

        # Get tweet text
        if 'extended_tweet' in response:
            tweet_text = response['extended_tweet']['full_text']
        else:
            tweet_text = response['text']

        # Associate each company mentioned with the tweet
        companies_mentioned = self.get_companies(tweet_text)
        for corp in companies_mentioned:
            #print(corp)
            #print(map1[corp])
            #response['company_name'] = corp
            response['ticker'] = map1[corp]
            producer.send(TOPIC_NAME, response)
            #print(response)

    def on_error(self, status_code):
        """
        Returning false disconnects the stream.
        """
        if status_code == 420:
            return False

# Start the Stream
if __name__ == "__main__":
    # Configuration for Kafka

    TOPIC_NAME = 'tweet'
    KAFKA_SERVER = 'kafka-1:9092'
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Open connection to Twitter API
    stream = TwitterStream(
        API_KEY, API_KEY_SECERT,
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    #print("producer is producing...")
    stream.filter(track=['Google'], languages=['en'])
    producer.flush()