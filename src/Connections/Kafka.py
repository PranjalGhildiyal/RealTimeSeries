from kafka import KafkaConsumer
import json
import pandas as pd
from RealTimeSeries.src.Logger.AppLogger import Applogger
from RealTimeSeries.configurations.index import read_section


class Connection:
    def __init__(self):
        status, logging_location= read_section('LOCATIONS')
        self.data= pd.DataFrame()
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        global lg
        global logger
        logger= Applogger(logging_location['kafka'])
        lg= logger.logger
        self.__connection_status = False
        self.__import_status = False
        status, self.configs = read_section('KAFKA')
        if not status:
            print('Could not find section: KAFKA')
            lg.error('Could not find section: KAFKA')
            return None

        lg.info('Initiating Connection with Kafka.')

    def connect(self, broker, topic):

        try:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[broker],
                value_deserializer=Connection.deserializer
            )
            lg.info(f'Connected to Kafka topic: {topic}')
            self.topic= topic
            self.__connection_status = True
            return self.__connection_status
        
        except Exception as e:
            lg.error(f'Failed to connect to Kafka: {str(e)}')
            return self.__connection_status

    def get_schema(self):
        status= False
        if self.__connection_status:
            try:
                for message in self.consumer:
                    status= True
                    all_keys= Connection.flatten_nested_dictionary_keys(message.value)
                    return (status, all_keys)
            except Exception as e:
                lg.error('Error while trying to get schema!')
                status= False
                return (status, 'Error while trying to get schema!')
        else:
            lg.error('No Connections found!')
            return (status, 'No Connections found!')

    def import_data(self, datetime_column, value_column, update_callback):
        if self.__connection_status == True:
            try:
                for message in self.consumer:
                    self.__import_status= True
                    req= dict(message.value)
                    req= Connection.flatten_nested_dictionary(message.value)
                    mframe = pd.DataFrame(req, index=[0])[[datetime_column, value_column]].rename(columns={datetime_column: 'DATETIME', value_column: 'value'})
                    yield mframe

                    # status= update_callback(mframe)
                    # if not status:
                    #     return self.__import_status
            except Exception as e:
                lg.error(f'Error while consuming messages: {str(e)}')
        else:
            lg.warning('Not connected to Kafka. Call connect() first.')
    
    def shutdown(self):
        logger.shutdown()

    def disconnect(self):
        if self.__connection_status:
            self.consumer.close()
            lg.info('Disconnected from Kafka.')
            self.__connection_status = False
            self.__import_status= False
        else:
            lg.warning('Not connected to Kafka.')


    @staticmethod
    def deserializer(value):
        return json.loads(value.decode('utf-8'))
    
    @staticmethod
    def flatten_nested_dictionary(nested_dict, separator='.'):
        flat_dict = {}
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                flat_subdict = Connection.flatten_nested_dictionary(value, separator=separator)
                for subkey, subvalue in flat_subdict.items():
                    flat_dict[f"{key}{separator}{subkey}"] = subvalue
            else:
                flat_dict[key] = value
        return flat_dict
    
    @staticmethod
    def flatten_nested_dictionary_keys(nested_dict, separator='.'):
        flat_dict = {}
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                flat_subdict = Connection.flatten_nested_dictionary(value, separator=separator)
                for subkey, subvalue in flat_subdict.items():
                    flat_dict[f"{key}{separator}{subkey}"] = subvalue
            else:
                flat_dict[key] = value
        return list(flat_dict.keys())
    
    def __str__(self):
        return {
                'Bootstrap Servers': self.configs['bootstrap_servers'],
                'Topic:': self.topic,
                'Connection Status': self.__connection_status,
                'Import Status': self.__import_status
                }

