from request_parameters import * 
from keys import *
from last_request_date import *

import datetime
import time

from kafka import KafkaProducer


from pathlib import Path

# Get articles
if __name__=="__main__":
    # Kafka definition
    TOPIC_NAME = 'stock_data'
    KAFKA_SERVER = 'localhost:9092' # TODO: check if right port for docker-compose.yml file
    #producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print('Under construction:', TOPIC_NAME)
