import panel as pn


from RealTimeSeries.configurations.index import read_section
class Dashboard:
    def __init__(self):
        _, db_configs= read_section('SQLDB')
        _, kafka_configs= read_section('KAFKA')

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
        self.db_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        database_bunch= pn.Column(
                                    pn.Row(self.sql_username, self.sql_password),
                                    self.sql_ip,
                                    pn.Row(self.sql_port, self.sql_database),
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
        self.filesystem_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        filesystem_bunch= pn.Column(self.file_input, self.sheet_name, self.filesystem_go, sizing_mode= 'stretch_width')

        # Making a clear button
        self.clear= pn.widgets.Button(name= 'CLEAR', button_type='danger', sizing_mode= 'stretch_width')

        # Adding watcher functions to go and clear buttons



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
        
        # Making main
        # self.gauge= pn.indicators.Gauge(name='Failure Rate', value=10, format= '{value}')
        # self.bars= pn.pane.Plotly()
        # self.pie_chart= pn.pane.Plotly()
        


        pn.serve(self.template)
        