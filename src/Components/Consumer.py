from time import sleep
from kafka import KafkaConsumer
import json
import pandas as pd

class Consumer:
    def __init__(self, topic, bootstrap_servers= ['localhost:9092'] )

        self.consumer = KafkaConsumer('transactions',
                                group_id='real-time-series',
                                bootstrap_servers=bootstrap_servers,
                                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                auto_offset_reset='earliest',
                                enable_auto_commit=False)

for message in consumer:
    mframe = pd.DataFrame(message.value)

    # Multiply the quantity by the price and store in a new "revenue" column
    mframe['revenue'] = mframe['Quantity'] * mframe['Price']
    
    # Aggregate the StockCodes in the individual batch by revenue
    summary = mframe.groupby('StockCode')['revenue'].sum()

    print(summary)