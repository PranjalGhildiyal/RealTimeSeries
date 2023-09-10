import pandas as pd
import logging as lg
import os


class Applogger():
    def __init__(self, log_file_location, timezone = 'Asia/Kolkata'):
        self.timezone = timezone
        self.login = pd.to_datetime(pd.Timestamp.now(tz= timezone).strftime('%Y-%m-%d %H:%M:%S'))
        self.log_file_location= log_file_location
        print(self.log_file_location)

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