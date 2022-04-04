from json import loads, dumps
from google.cloud import storage
from kafka import KafkaConsumer
from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
from sentiment import *

def getconn() -> pg8000.native.Connection:
    """
    :return: Connection to the 'stonks' db on the GCP Postgres instance
    """
    conn: pg8000.native.Connection = connector.connect(
        "stonks-343022:us-central1:stock-stack",
        "pg8000",
        user="postgres",
        password="darpatliznikjuschi",
        db="stonks"
    )
    return conn


# kafka configuration
TOPIC_NAME = 'stock_data'
KAFKA_SERVER = 'localhost:9092'
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers = KAFKA_SERVER,
                         value_deserializer = lambda m : loads(m.decode('utf-8')))

# google cloud storage configuration
bucket_name = 'stonks_chilly_storage'
destination_blob_name = 'twitter_stream'
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

# get pooled connection to cloud postgres instance
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# upload data from the stream to the bucket and postgres
with pool.connect() as db_conn:
    for message in consumer:
        # get tweet as json
        tweet = dumps(message.value)

        # stream to the storage bucket
        blob.upload_from_string(tweet)

        # get sentiment score for the tweet
        tweet_sentiment = SentimentAnalyzer(tweet['text'])
        tweet_sentiment.run_sentiment_analysis()
        sentiment_scores = ???

        # insert into postgres db
        # INSERT STATEMENT GOES HERE
