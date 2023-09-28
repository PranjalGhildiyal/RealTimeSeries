from RealTimeSeriesDev.configurations.index import read_section
from RealTimeSeriesDev.src.CustomModels.Model import EnquiryEngine, ModelArchive

#===========================================================
#                         Step 1
#============================================================
# Read all configs here.

class ConfigReader:
    def __init__(self):
        print('in ConfigReader')
        _, self.db_configs= read_section('SQLDB')
        _, self.kafka_configs= read_section('KAFKA')
        _, self.sharepoint_configs= read_section('SHAREPOINT')


        # Importing custom models
        self.inquiry= EnquiryEngine()
