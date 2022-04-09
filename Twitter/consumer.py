from json import loads, dumps
from google.cloud import storage
from kafka import KafkaConsumer
from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
from sentiment import *

# def getconn() -> pg8000.native.Connection:
#     """
#     :return: Connection to the 'stonks' db on the GCP Postgres instance
#     """
#     conn: pg8000.native.Connection = connector.connect(
#         "stonks-343022:us-central1:stock-stack",
#         "pg8000",
#         user="postgres",
#         password="darpatliznikjuschi",
#         db="stonks"
#     )
#     return conn


# kafka configuration
TOPIC_NAME = 'stock_data'
KAFKA_SERVER = 'localhost:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers = KAFKA_SERVER,
                         value_deserializer = lambda m : loads(m.decode('utf-8')))

# google cloud storage configuration
# bucket_name = 'stonks_chilly_storage'
# destination_blob_name = 'twitter_stream'
# storage_client = storage.Client()
# bucket = storage_client.bucket(bucket_name)
# blob = bucket.blob(destination_blob_name)

# get pooled connection to cloud postgres instance
# pool = sqlalchemy.create_engine(
#     "postgresql+pg8000://",
#     creator=getconn,
# )

# upload data from the stream to the bucket and postgres
# with pool.connect() as db_conn:
for message in consumer:
    # get tweet as json
    tweet_object = dumps(message.value)

    # stream to the storage bucket
    # blob.upload_from_string(tweet_object)

    # get text of the tweet
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

    if compound_sentiment == 0.0:
        sentiment_class = 'neutral'
    elif compound_sentiment < 0.0:
        sentiment_class = 'negative'
    else:
        sentiment_class = 'positive'

    no_followers = message.value['user']['followers_count']

    # print stuff that stored in Postgres
    # print(tweet_text)
    # print(f"compound sentiment score: {compound_sentiment}")
    # print(f'sentiment class: {sentiment_class}')
    # print(f"no. followers: {no_followers}")

    # insert into postgres db
    # INSERT STATEMENT GOES HERE
