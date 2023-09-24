from configurations.index import read_section

#===========================================================
#                         Step 1
#============================================================
# Read all configs here.


class ConfigReader:
    '''
    Class ConfigReader
    - Extracts configurations from the config.ini file.
    '''
    def __init__(self):
        _, self.db_configs= read_section('SQLDB')
        _, self.kafka_configs= read_section('KAFKA')
        _, self.sharepoint_configs= read_section('SHAREPOINT')
