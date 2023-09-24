import pandas as pd
from configurations.index import read_section
from src.Logger.AppLogger import Applogger
import os
from io import BytesIO
import time

class Connection:
    def __init__(self):
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        global lg
        global logger
        logger= Applogger(logging_location['filesystem'])
        lg= logger.logger
        lg.info('Initiated File Import.')

    def connect(self, path, format, sheet_name, separator):
        '''
        returns the scema only for the user to select the datetime column and the value column in the modal!!
        '''
        status= False
        self.sheet_name= sheet_name
        self.separator= separator
        self.format= format
        try:
            self.file= BytesIO(path)
            print(self.file)
            status= True
            lg.info('Connected to file path!')
            return status
        except Exception as e:
            lg.error(f'Error while connecting to filesystem. Error message: {str(e)}')
            return status
        
    def get_schema(self):
        status= False
        if self.format == 'xlsx':
            data= pd.read_excel(self.file, nrows=1, header= None).loc[0]
            lg.info('Schema imported successfully!')
            status= True
            return (status, list(data.values))
        elif self.format == 'csv':
            data= pd.read_csv(self.file, nrows=1, header= None).loc[0]
            # Resetting the bytes object cursor to 0th position
            self.file.seek(0)
            lg.info('Schema imported successfully!')
            status= True
            return (status, list(data.values))

    
    def import_data(self, timestamp_column, value_column, callback):
        status= False
        if self.format == 'xlsx':
            if self.sheet_name is not None:
                data= pd.read_excel(self.file, sheet_name=self.sheet_name, usecols=[timestamp_column, value_column]).rename(columns={timestamp_column: 'DATETIME', value_column:  'value'})
            else:
                data = pd.read_excel(self.file, usecols=[timestamp_column, value_column]).rename(columns={timestamp_column: 'DATETIME', value_column:  'value'})
            status= True
            lg.info('Data imported successfully!')
            for i in data.index:
                yield pd.DataFrame(data.loc[i]).T
        
        elif self.format == 'csv':
            self.file.seek(0)
            if self.separator is not None:
                data= pd.read_csv(self.file, sep= self.separator, usecols=[timestamp_column, value_column]).rename(columns={timestamp_column: 'DATETIME', value_column: 'value'})
            else:
                data= pd.read_csv(self.file, usecols=[timestamp_column, value_column]).rename(columns={timestamp_column: 'DATETIME', value_column: 'value'})
            status= True
            lg.info('Data imported successfully!')
            for i in data.index:
                yield pd.DataFrame(data.loc[i]).T
        
    def shutdown(self):
        logger.shutdown()

    @property
    def bytes_obj(self):
        return self.file