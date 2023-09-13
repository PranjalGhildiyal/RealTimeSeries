import pandas as pd
from RealTimeSeries.configurations.index import read_section
from RealTimeSeries.src.Logger.AppLogger import Applogger
import os
from io import BytesIO

class Connection:
    def __init__(self):
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not find section. {}'.format(logging_location))
            return None
        global lg
        lg= Applogger(logging_location['filesystem']).logger

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
            status= True
            return status
        except Exception as e:
            lg.error(f'Error while connecting to filesystem. Error message: {str(e)}')
            return status
        
    def get_schema(self):
        status= False
        if self.format == 'xlsx':
            data= pd.read_excel(self.file, nrows=1, header= None).loc[0]
            status= True
            return (status, list(data.values))
        elif self.format == 'csv':
            data= pd.read_csv(self.file, nrows=1, header= None).loc[0]
            status= True
            return (status, list(data.values))

    
    def import_data(self):
        status= False
        if self.format == 'xlsx':
            data= pd.read_excel(self.file, sheet_name=self.sheet_name)
            status= True
            return (status, data)
        elif self.format == 'csv':
            data= pd.read_csv(self.file, sep= self.separator)
            status= True
            return (status, data)