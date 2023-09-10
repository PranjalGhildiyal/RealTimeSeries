import requests
import pandas as pd
import io
from RealTimeSeries.src.Logger.AppLogger import Applogger
from RealTimeSeries.configurations.index import read_section


class Connection:
    def __init__(self, url):
        self.url = url
        self.is_valid = False  # Initialize a flag for valid connection
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        global lg
        lg= Applogger(logging_location['url']).logger
        self.__connection_status = 'Disconnected'
        self.__import_status = False
        self.data= None

        lg.info('Initiating Connection with Kafka.')

    def test_connection(self):
        try:
            # Send a HEAD request to the URL to check if it's reachable
            response = requests.head(self.url)
            
            # Check if the request was successful (status code 200 indicates success)
            if response.status_code == 200:
                self.is_valid = True
                lg.info('Connection test successful.')
            else:
                lg.warning(f'Connection test failed. Status code: {response.status_code}')
        except Exception as e:
            lg.error(f'Error testing connection: {str(e)}')

        return self.is_valid
    
    def download_data(self):
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(self.url)

            # Check if the request was successful (status code 200 indicates success)
            if response.status_code == 200:
                # Get the content (data) from the response
                self.data = response.content
                lg.info('Data downloaded successfully.')
            else:
                lg.warning(f'Failed to download data. Status code: {response.status_code}')
        except Exception as e:
            lg.error(f'Error downloading data: {str(e)}')

    def get_data_as_dataframe(self):
        if self.data is not None:
            try:
                # Assuming the data is in CSV format, you can adjust this part as needed
                data_str = self.data.decode('utf-8')
                df = pd.read_csv(io.StringIO(data_str))
                return df
            except Exception as e:
                lg.info(f'Error converting data to DataFrame: {str(e)}')
                return None
        else:
            lg.error('No data available to convert to DataFrame.')
            return None
