import pandas as pd

class Connection:
    def __init__(self, path, sheet_name):
        self.filepath= path
        self.format= self.filepath.split('.')[-1]
        self.sheet_name= sheet_name

    def connect(self):
        '''
        returns the scema only for the user to select the datetime column and the value column in the modal!!
        '''
        if self.format == 'xlsx':
            data= pd.read_excel(self.filepath, nrows=1, header= None).loc[0]
            return data
        elif self.format == 'csv':
            data= pd.read_csv(self.filepath, nrows=1, header= None).loc[0]
            return data
    
    def import_file(self):
        if self.format == 'xlsx':
            data= pd.read_excel(self.filepath, nrows=1, header= None).loc[0]
            return data
        elif self.format == 'csv':
            data= pd.read_csv(self.filepath, nrows=1, header= None).loc[0]
            return data