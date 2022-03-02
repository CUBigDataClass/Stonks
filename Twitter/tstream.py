from tweepy import Stream
import json
from keys import *
from kafka import KafkaProducer


class TwitterStream(Stream):
    """
    Inherits from tweepy's Stream class. We are only modifying the few functions
    we need to customize, namely what to do when new tweets come through.
    """

    # Kafka definition
    TOPIC_NAME = 'stock_data'
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

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
        producer.send(TOPIC_NAME, response)

    def on_error(self, status_code):
        """
        Returning false disconnects the stream.
        """
        if status_code == 420:
            return False

# Start the Stream
if __name__ == "__main__":
    TOPIC_NAME = 'stock_data'
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Open connection to Twitter API
    stream = TwitterStream(
        API_KEY, API_KEY_SECERT,
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    print("producer is running...")
    stream.filter(track=['Microsoft'], languages=['en'])
    producer.flush()

