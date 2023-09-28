import os
import pandas as pd
import importlib
from dataclasses import dataclass
from RealTimeSeriesDev.configurations.index import read_section
from RealTimeSeriesDev.src.Logger.AppLogger import Applogger
from RealTimeSeriesDev.src.Exceptions.index import *

class ModelArchive:
    def __init__(self):
        _, info= read_section('INFO')
        custom_models_directory= info['custom_models_directory']

        _, self.paths= read_section('LOCATIONS')
        path = self.paths['models']

        # Initiating Applogger

        self.logger= Applogger(path)
        self.lg= self.logger.logger


        self.file_list= pd.Series(os.listdir(custom_models_directory))
        self.lg.info('Modules found: {}'.format(self.file_list))
        self.file_list= self.file_list[(self.file_list != 'Model.py') & (self.file_list != '__pycache__')]
        self.lg.info('Relevant modules found: {}'.format(self.file_list))
        

        self.classes= {}
        for model_type in self.file_list:
            try:
                model_name= model_type.split('.')[0]
                # Use importlib to import the module dynamically
                spec = importlib.util.spec_from_file_location(model_type, os.path.join(custom_models_directory, model_type))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.classes[model_name] = module
                self.lg.info('{} imported successfully'.format(model_name))
            except Exception as e:
                self.lg.error(ErrorWithCustomModel(model_type, e))


@dataclass
class EnquiryEngine:
    archive= ModelArchive()
    lg= archive.lg

    @property
    def available_models(self):
        return list(self.archive.classes.keys())
    
    def get_model(self, model_type):
        return self.archive.classes[model_type].Model()


@dataclass
class ModelDetails:
    model_type: str
    enquiry_engine= EnquiryEngine()
    lg= enquiry_engine.lg
    
    @property
    def model(self):
        if self.model_type not in self.enquiry_engine.available_models:
            self.lg.error(InvalidModelException)
            raise InvalidModelException
        return self.enquiry_engine.get_model(self.model_type)
    
        
    
    
        



        


        
        



