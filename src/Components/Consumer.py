from kafka import KafkaConsumer
import json
import pandas as pd

class Consumer:
    def __init__(self, topic, bootstrap_servers= ['localhost:9092']):

        self.consumer = KafkaConsumer(topic,
                                bootstrap_servers=bootstrap_servers,
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                auto_offset_reset='earliest',
                                enable_auto_commit=False)
        self.topic= topic

    def stream(self):
        return self.consumer