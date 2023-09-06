import pandas as pd
import json
import datetime as dt
from time import sleep
from kafka import KafkaProducer



class Producer:
    def __init__(self, topic, bootstrap_servers= ['localhost:9092']):
        self.topic= topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    
    def stream(self, value:dict, key=None):
        # Converting value dict to json
        value= json.dumps(value, default=str)
        #Encoding to 'utf8'
        value= value.encode('utf-8')
        if key:
            key= str(key).encode('utf-8')
        self.producer.send(topic=self.topic, key=key, value=value)