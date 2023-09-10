from kafka import KafkaConsumer
import json
import pandas as pd
from RealTimeSeries.src.Logger.AppLogger import Applogger
from RealTimeSeries.configurations.index import read_section
import asyncio


class Connection:
    def __init__(self):
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        global lg
        lg= Applogger(logging_location['kafka']).logger
        self.__connection_status = 'Disconnected'
        self.__import_status = False
        status, self.configs = read_section('KAFKA')
        if not status:
            print('Could not find section: KAFKA')
            lg.error('Could not find section: KAFKA')
            return None

        lg.info('Initiating Connection with Kafka.')

    def connect(self, topic):
        print(self.configs)
        try:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[self.configs['bootstrap_servers']],
                value_deserializer=Connection.deserializer
            )
            print('Done')
            lg.info(f'Connected to Kafka topic: {topic}')
            self.topic= topic
            self.__connection_status = 'Connected'
        except Exception as e:
            lg.error(f'Failed to connect to Kafka: {str(e)}')

    async def consume_and_update_plots(self, update_callback=None):
        if self.__connection_status == 'Connected':
            try:
                for message in self.consumer:
                    self.__import_status= True
                    mframe = pd.DataFrame(message.value, index=[0])
                    
                    # Call the update_callback function with self.values as input
                    if update_callback:
                        await update_callback(mframe)
            except Exception as e:
                lg.error(f'Error while consuming messages: {str(e)}')
        else:
            lg.warning('Not connected to Kafka. Call connect() first.')

    def disconnect(self):
        if self.__connection_status == 'Connected':
            self.consumer.close()
            lg.info('Disconnected from Kafka.')
            self.__connection_status = 'Disconnected'
            self.__import_status= False
        else:
            lg.warning('Not connected to Kafka.')


    @staticmethod
    def deserializer(value):
        return json.loads(value.decode('utf-8'))
    
    def __str__(self):
        return {
                'Bootstrap Servers': self.configs['bootstrap_servers'],
                'Topic:': self.topic,
                'Connection Status': self.__connection_status,
                'Import Status': self.__import_status
                }

