import panel as pn
from RealTimeSeries.configurations.index import read_section
from RealTimeSeries.src.Connections import DataBase, Kafka, SystemFiles, url
import time
class Dashboard:
    def __init__(self):
        _, db_configs= read_section('SQLDB')
        _, kafka_configs= read_section('KAFKA')

        # Defining important
        self.datetime_column_selector= pn.widgets.Select(name= 'Select datetime column')
        self.value_selector= pn.widgets.Select(name= 'Select value column')
        self.connection_status= pn.indicators.LoadingSpinner(value=False, color='primary', bgcolor='dark')

        last_n= pn.widgets.IntInput(name='Enter `n`', value=1, sizing_mode= 'stretch_width')
        last_unit= pn.widgets.Select(name= 'Select unit', options= ['minutes', 'hours', 'seconds', 'days', 'months', 'years'], value='minutes', sizing_mode= 'stretch_width')
        n_indexes= pn.widgets.IntInput(name='Enter number of observations to display', sizing_mode= 'stretch_width', value= 100)
        self.config_widgetbox= pn.WidgetBox(pn.Column(pn.Row(last_n, last_unit), n_indexes), sizing_mode= 'stretch_width')

        # Making database section
        self.sql_username=pn.widgets.TextInput(name= 'sql_username', value=db_configs['sql_username'], sizing_mode= 'stretch_width')
        self.sql_password=pn.widgets.PasswordInput(name='Password', placeholder='Enter passsword', sizing_mode= 'stretch_width', value= db_configs['sql_password'])
        self.sql_ip=pn.widgets.TextInput(name= 'sql_ip', value=db_configs['sql_ip'], sizing_mode= 'stretch_width')
        self.sql_port=pn.widgets.TextInput(name= 'sql_port', value=db_configs['sql_port'], sizing_mode= 'stretch_width')
        self.sql_database=pn.widgets.TextInput(name= 'sql_username', value=db_configs['sql_database'], sizing_mode= 'stretch_width')
        self.sql_db_tablename= pn.widgets.TextInput(name='Enter table name', value='', sizing_mode= 'stretch_width')
        self.db_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        database_bunch= pn.Column(
                                    pn.Row(self.sql_username, self.sql_password),
                                    self.sql_ip,
                                    pn.Row(self.sql_port, self.sql_database),
                                    self.sql_db_tablename,
                                    self.db_go,
                                    sizing_mode= 'stretch_width'
                                )

        # Making Kafka Section
        self.bootstrap_servers= pn.widgets.TextInput(name= 'bootstrap_servers', placeholder=str([kafka_configs['bootstrap_servers']]), sizing_mode= 'stretch_width')
        self.topics= pn.widgets.TextInput(name='Enter topic name', sizing_mode= 'stretch_width')
        self.kafka_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        kafka_bunch= pn.Column(self.bootstrap_servers, self.topics, self.kafka_go, sizing_mode= 'stretch_width')

        # Making url section
        self.url_input= pn.widgets.TextInput(name= 'Enter URL', sizing_mode= 'stretch_width')
        self.url_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        url_bunch= pn.Column(self.url_input, self.url_go)

        # Making Filesystem section
        self.file_input = pn.widgets.FileInput(accept='.csv, .xlsx', multiple= False, sizing_mode='stretch_width')
        self.sheet_name= pn.widgets.TextInput(name= 'sheet_name', placeholder= 'Enter sheetname if using an excel worksheet.', value= None)
        self.separator= pn.widgets.TextInput(name= 'Separator', placeholder= 'No default', value=None)
        self.filesystem_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        filesystem_bunch= pn.Column(self.file_input, self.sheet_name, self.separator, self.filesystem_go, sizing_mode= 'stretch_width')

        # Making a clear button
        self.clear= pn.widgets.Button(name= 'CLEAR', button_type='danger', sizing_mode= 'stretch_width')

        # Adding watcher functions to go and clear buttons
        self.db_go.on_click(self.__db_connect)
        self.filesystem_go.on_click(self.__filesystem_connect)



        # Making Accordion
        accordion= pn.Accordion(
                                ('SQL Database', database_bunch),
                                ('Apache Kafka', kafka_bunch),
                                ('URL', url_bunch),
                                ('System Files', filesystem_bunch),
                                sizing_mode= 'stretch_width'
                                )
        
        # Now finally making a sidebar
        self.sidebar= pn.Column(
                                    self.config_widgetbox,
                                    accordion,
                                    self.clear
                                )
        
        # Now making the main body



        # Template decision
        self.template = pn.template.BootstrapTemplate(
                                                        title="Clinician",
                                                        sidebar=self.sidebar,
                                                        theme= 'dark'
                                                    )
        self.template.modal.append(pn.Column())
        
        # Making main
        self.gauge= pn.indicators.Gauge(name='Failure Rate', value=10, format= '{value}')
        self.bars= pn.pane.Plotly()
        self.pie_chart= pn.pane.Plotly()
        


        pn.serve(self.template)


    def __db_connect(self, event=None):
        self.db_go.button_type= 'success'
        self.connection_status.value= True
        self.template.modal[0].clear()
        self.template.modal[0].append(
                                        pn.Row(
                                            pn.layout.HSpacer(),
                                            self.connection_status,
                                            pn.layout.HSpacer()
                                            )
        )
        self.template.open_modal()
        self.connection= DataBase.Connection()
        status= self.connection.connect(self.sql_username.value, self.sql_password.value, self.sql_ip.value, self.sql_port.value, self.sql_database.value)
        if status:
            
            columns= self.connection.get_schema(self.sql_db_tablename.value)
            if columns== []:
                self.connection_status.value= False
                self.template.modal[0].append(pn.pane.Alert('The table doen not exist in the database. Check the table name and database credentials!', alert_type= 'danger'))
                time.sleep(4)
                self.template.close_modal()
            else:
                self.datetime_column_selector.options= columns
                self.value_selector.options= columns
                start_importing= pn.widgets.Button(name= 'GO', button_type= 'primary')
                start_importing.on_click(self.__begin_showcase)
                self.template.modal[0].append(pn.Column(pn.Row(self.datetime_column_selector, self.value_selector), start_importing))

        
    def __apache_connect(self, event=None):
        self.db_go.button_type= 'success'
        self.connection_status.value= True
        self.template.modal[0].clear()
        self.template.modal[0].append(
                                      pn.Row(
                                            pn.layout.HSpacer(),
                                            self.connection_status,
                                            pn.layout.HSpacer()
                                            )
        )
        self.template.open_modal()
        self.connection= DataBase.Connection()
        status= self.connection.connect(self.sql_username.value, self.sql_password.value, self.sql_ip.value, self.sql_port.value, self.sql_database.value)
        if status:
            
            columns= self.connection.get_schema(self.sql_db_tablename.value)
            if columns== []:
                self.connection_status.value= False
                self.template.modal[0].append(pn.pane.Alert('The table doen not exist in the database. Check the table name and database credentials!', alert_type= 'danger'))
                time.sleep(4)
                self.template.close_modal()
            else:
                self.datetime_column_selector.options= columns
                self.value_selector.options= columns
                start_importing= pn.widgets.Button(name= 'GO', button_type= 'primary')
                start_importing.on_click(self.__begin_showcase)
                self.template.modal[0].append(pn.Column(pn.Row(self.datetime_column_selector, self.value_selector), start_importing))

    def __filesystem_connect(self, event=None):
        print(self.file_input.value)
        self.connection= SystemFiles.Connection(self.file_input.value, self.sheet_name.value)
        schema= self.connection.connect()

        
    
    def __begin_showcase(self, event=None):
        self.template.modal[0].append(pn.pane.Alert('Successfully Imported Data!', alert_type='success'))
        self.connection_status.value= False
        time.sleep(4)
        self.template.close_modal()
        pass
        



        