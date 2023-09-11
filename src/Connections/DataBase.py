import pandas as pd
import configparser
from sqlalchemy import create_engine
from RealTimeSeries.src.Logger.AppLogger import Applogger
from RealTimeSeries.configurations.index import read_section
    

class Connection:
    def __init__(self):
        status, logging_location= read_section('LOCATIONS')
        if not status:
            print('Could not finf section. {}'.format(logging_location))
            return None
        global lg
        lg= Applogger(logging_location['sqldb']).logger
        self.__connection_status= 'Disconnected'
        self.__import_status= False
        self.__engine= None
        _, timezone= read_section('INFO')
        timezone= timezone['timezone']
        _, self.configs= read_section('SQLDB')
        self.connection_time= pd.to_datetime(pd.Timestamp.now(tz= timezone).strftime('%Y-%m-%d %H:%M:%S'))
        lg.info('Initiating Connection with Database.')

    def connect(self, sql_username:str='', sql_password:str='', sql_ip:str='', sql_port:str='', sql_database:str='')->str:
        if any(val == '' for val in [sql_username, sql_password, sql_ip, sql_port, sql_database]):
            sql_username, sql_password, sql_ip, sql_port, sql_database= self.configs['sql_username'], self.configs['sql_password'], self.configs['sql_ip'], self.configs['sql_port'], self.configs['sql_database']
        
        lg.info("Start for making sql_conn with %s, %s, %s, %s, %s" , sql_username, sql_password, sql_ip, sql_port, sql_database)
        try:
            if sql_port == "0" or sql_port == 0:
                sql_port = "3306"
            connect_query = "mysql+pymysql://"+sql_username+":"+sql_password+"@"+sql_ip+":"+sql_port+"/"+sql_database
            self.__engine = create_engine(connect_query)
            self.__connection_status= 'Connected'
            lg.info("Execution success with engine: %s", self.__engine)
            return self.__connection_status
        except Exception as e:
            lg.error("Execution failure")
            lg.exception("Exception: " + str(e))
            return self.__connection_status
        
    def get_schema(self, table_name:str):
        query= '''SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{}'
                    ORDER BY ORDINAL_POSITION'''.format(table_name.value)
        columns= pd.read_sql(query, self.__engine)
        return list(columns['COLUMN_NAME'].values)

    
    def import_table(self, table_name:str, timestamp_column:str, value_column:str):
        query= 'select {},{} from {}.{}'.format(timestamp_column, value_column, self.configs['sql_database'], table_name)
        lg.info("Downloading data from database. Query:  %s, Engine: %s" , query,self.__engine)
        try:
            data = pd.read_sql(query,self.__engine)
            self.imported_data= data.rename(columns= {timestamp_column: 'DATETIME', value_column:'value'})
            self.__import_status= True
            lg.info("Data imported from database successfully.")
            return self.__import_status
        except Exception as e:
            lg.error("Execution failure")
            lg.exception("Exception: " + str(e))
            return self.__import_status

    @property
    def connection_status(self):
        return self.__connection_status

    @property
    def engine(self):
        return self.__engine
    
    @property
    def import_status(self):
        return self.__import_status
    
    def reconnect(self):

        self.connect()
        return self.__connection_status


    def __str__(self):
        return {'Connection:': self.__connection_status,
                'Engine': self.__engine,
                'Database Configs': self.configs,
                }

