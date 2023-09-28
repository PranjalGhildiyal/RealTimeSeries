import requests
import pandas as pd
import io
from RealTimeSeriesDev.src.Logger.AppLogger import Applogger
from RealTimeSeriesDev.configurations.index import read_section
import time


class Connection:
    def __init__(self, url):
        self.url = url
        self.__connection_status = False  # Initialize a flag for valid connection
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        
        self.logger= Applogger(logging_location['url'])
        self.lg= self.logger.logger
        self.__import_status = False
        self.data= None

        self.lg.info('Initiating Connection with Kafka.')

    def connect(self):
        try:
            # Send a HEAD request to the URL to check if it's reachable
            response = requests.head(self.url)
            
            # Check if the request was successful (status code 200 indicates success)
            if response.status_code == 200:
                self.__connection_status = True
                self.lg.info('Connection test successful.')
            else:
                self.lg.warning(f'Connection test failed. Status code: {response.status_code}')
        except Exception as e:
            self.lg.error(f'Error testing connection: {str(e)}')

        return self.__connection_status
        
    def get_schema(self):
        status= False
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(self.url)

            # Check if the request was successful (status code 200 indicates success)
            if response.status_code == 200:
                # Get the content (data) from the response
                try:
                    self.data = response.content
                    data_str = self.data.decode('utf-8')
                    self.data = pd.read_csv(io.StringIO(data_str))
                    self.lg.info('Data downloaded successfully.')
                    status= True
                    return (status, list(self.data.columns))
                except Exception as e:
                    self.data = None
                    self.lg.warning(f'Failed to convert data to readable dataframe.')
                    return (status, f'Failed to convert data to readable dataframe.')

            else:
                 self.lg.error(f'Failed to get data. Status code: {response.status_code}')
                 return (status, f'Failed to get data. Status code: {response.status_code}')
                 
        except Exception as e:
            self.lg.error(f'Error downloading data: {str(e)}')
            return (status, f'Error downloading data: {str(e)}')

    def import_data(self, timestamp_column, value_column, callback):
        status= False
        if self.data is not None:
            status= True
            self.data= self.data.rename(columns={timestamp_column: 'DATETIME', value_column: 'value'})[['DATETIME', 'value']]
            for i in self.data.index:
                yield pd.DataFrame(self.data.loc[i]).T
        else:
            self.lg.error('No data available to convert to DataFrame.')
            return (status, 'No data available to convert to DataFrame.')

    def shutdown(self):
        self.logger.shutdown()
