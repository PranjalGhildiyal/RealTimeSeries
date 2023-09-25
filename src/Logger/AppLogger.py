import pandas as pd
import logging as lg
import os
from configurations.index import read_section


class Applogger():
    '''class Applogger: custom Logger class for RealTImeSeries App.
        - property: logger
            - returns logger initialized for that particular connection method. 
            - Can be used to log in the directory mentioned in config.ini
        - property: shutdown
            - shuts the connection down to prevent duplicate entries in the log file.'''
    def __init__(self, log_file_location):

        _, app_info= read_section('INFO')
        if not _:
            self.timezone= 'Asia/Kolkata'
        else:
            self.timezone= app_info['timezone']

        self.login = pd.to_datetime(pd.Timestamp.now(tz= self.timezone).strftime('%Y-%m-%d %H:%M:%S'))
        self.log_file_location= log_file_location
        if not os.path.exists('Logs'):
            os.mkdir('Logs')

    @property
    def logger(self):
        self._logger = lg.getLogger(__name__)
        self._logger.setLevel(lg.DEBUG)
        
        # Create a file handler for writing log messages to the specified log file
        file_handler = lg.FileHandler(self.log_file_location)
        
        # Create a formatter to define the log message format
        formatter = lg.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self._logger.addHandler(file_handler)
        return self._logger
    
    def shutdown(self):
        self._logger.warning('Deleting logger instance. \n')
        lg.shutdown()
        self._logger.handlers.clear()