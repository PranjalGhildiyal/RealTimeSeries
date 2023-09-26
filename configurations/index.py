import configparser    
    
def read_section(section:str)->tuple:
    status= False
    try:
        config = configparser.ConfigParser()
        config.read(r'RealTimeSeriesDev/configurations/config_file.ini')
        config_sections  = config.sections()
        if section not in config_sections:
            return(status,"No such config found.")
        config_set= {}
        for key_config in config[section]:
                config_set[key_config] = config[section][key_config]
        status= True
        return(status, config_set)
    except Exception as e:
        status= False
        return (status,"Error message : {}.".format(str(e)))
    