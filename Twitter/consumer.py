from json import loads, dumps
from google.cloud import storage
from kafka import KafkaConsumer

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

# upload data from the stream to the bucket
for message in consumer:
    tweet = dumps(message.value)
    blob.upload_from_string(tweet)
    
