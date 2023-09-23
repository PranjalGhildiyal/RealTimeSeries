# Import your custom connector
try:
    from RealTimeSeries.src.Components.WidgetDefinitions import WidgetDefinitions
    from RealTimeSeries.src.Connections import DataBase, Kafka, SystemFiles, url
    import panel as pn
    import time
    import holoviews as hv
    import pandas as pd
    from pmdarima import arima
    from pmdarima import model_selection
    from pmdarima import pipeline
    from pmdarima import preprocessing
    from holoviews import opts
    import asyncio
except ImportError as import_error:
    print(f'Could not import module: {import_error}.')

#===========================================================
#                         Step 3
#============================================================
# Build customized widgets for your connector here

class ConnectionWidgets(WidgetDefinitions):
    def __init__(self):
        '''
        SYNTAX
        ======

        Step 3.1: Define buttons for input to a connector.
               - Structure of the connector:
                          - The connector should be a python class, stored  in `Connections` folder in the src folder.
                          - The connector should have four attributes:
                              -__init__(*init_connection_parameters): The __init__ function.
                              - connect(*connect_parameters): The method to connect. This should return a boolean True of False, based on the connection status.
                              -get_schema(*get_schema_parameters): Returns a tuple containing: 
                                                                                              1. `status`(bool) 
                                                                                              2. `column_names`(list)
                              -import_data(*import_data_parameters): Returns a tuple, containing:
                                                                                              1. `status`(bool) 
                                                                                              2. `data`(pd.DataFrame)
              - Dont forget to wrap all the relevant widgets in a widget bunch, which will be used later.
                  
        Step 3.2: Define input parameter list for each Step of the connector. The input parameters are holoviz panel widgets with the `value` attribute as parameters OR any other entity not having a `value` attribute.

        Step 3.3: Add watcher function in the syntax:
             self.your_custom_import_button_widget.on_click(lambda event: self.__combined_connector(Method.Connection, init_param_list, connect_param_list, get_schema_param_list, import_data_param_list, self.your_custom_import_button_widget))
        Steo 3.4: Add your widget bunch to the accordion as a tuple, with first element as the display name. eg: ('Display Name', widget_bunch)
        '''
        super().__init__() 
        print('in ConnectionWidgets')

        # -------------------------------------------------------------------------------------------------------------------------------------------------
        #                                                            CHANGE FROM HERE
        # -------------------------------------------------------------------------------------------------------------------------------------------------

        # -----------------database------------------------
        # Step 3.1
        self.sql_username=pn.widgets.TextInput(name= 'sql_username', value=self.db_configs['sql_username'], sizing_mode= 'stretch_width')
        self.sql_password=pn.widgets.PasswordInput(name='Password', placeholder='Enter passsword', sizing_mode= 'stretch_width', value= self.db_configs['sql_password'])
        self.sql_ip=pn.widgets.TextInput(name= 'sql_ip', value=self.db_configs['sql_ip'], sizing_mode= 'stretch_width')
        self.sql_port=pn.widgets.TextInput(name= 'sql_port', value=self.db_configs['sql_port'], sizing_mode= 'stretch_width')
        self.sql_database=pn.widgets.TextInput(name= 'sql_database', value=self.db_configs['sql_database'], sizing_mode= 'stretch_width')
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
        
        # Step 3.2:
        db_init_connection_parameters= []
        db_connect_parameters= [
            self.sql_username, 
            self.sql_password, 
            self.sql_ip, 
            self.sql_port, 
            self.sql_database
            ]
        db_get_schema_parameters= [self.sql_db_tablename]
        db_import_data_parameters= [self.datetime_column_selector, self.value_selector, self.catch_value]

        # Step 3.3:
        self.db_go.on_click(lambda event: self.__combined_connector(DataBase.Connection, db_init_connection_parameters, db_connect_parameters, db_get_schema_parameters, db_import_data_parameters, self.db_go))

        # -----------------ApacheKafka------------------------
        # Step 3.1
        self.kafka_broker= pn.widgets.TextInput(name= 'bootstrap_servers', placeholder=str([self.kafka_configs['bootstrap_servers']]), sizing_mode= 'stretch_width')
        self.kafka_topic= pn.widgets.TextInput(name='Enter topic name', sizing_mode= 'stretch_width')
        self.kafka_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        kafka_bunch= pn.Column(self.kafka_broker, self.kafka_topic, self.kafka_go, sizing_mode= 'stretch_width')

        # Step 3.2:
        kafka_init_connection_parameters= []
        kafka_connect_parameters = [self.kafka_broker, self.kafka_topic]
        kafka_get_schema_parameters = []
        kafka_import_data_parameters = [self.datetime_column_selector, self.value_selector, self.catch_value]

        # Step 3.3:
        self.kafka_go.on_click(lambda event: self.__combined_connector(Kafka.Connection, kafka_init_connection_parameters, kafka_connect_parameters, kafka_get_schema_parameters, kafka_import_data_parameters, self.kafka_go))

        # -----------------URL------------------------
        # Step 3.1:
        self.url_input= pn.widgets.TextInput(name= 'Enter URL', sizing_mode= 'stretch_width')
        self.url_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        url_bunch= pn.Column(self.url_input, self.url_go)

        # Step 3.2:
        url_init_connection_parameters= [self.url_input]
        url_connect_parameters = []
        url_get_schema_parameters = []
        url_import_data_parameters = [self.datetime_column_selector, self.value_selector, self.catch_value]

        # Step 3.3:
        self.url_go.on_click(lambda event: self.__combined_connector(url.Connection, url_init_connection_parameters, url_connect_parameters, url_get_schema_parameters, url_import_data_parameters, self.url_go))

        # #--------------FileSystem----------------------------
        # Step 3.1:
        self.file_input = pn.widgets.FileInput(accept='.csv, .xlsx', multiple= False, sizing_mode='stretch_width')
        self.sheet_name= pn.widgets.TextInput(name= 'sheet_name', placeholder= 'Enter sheetname if using an excel worksheet.', value= None)
        self.separator= pn.widgets.TextInput(name= 'Separator', placeholder= 'No default', value=None)
        self.format= pn.widgets.Select(name= 'Format Selected', value='csv', options=['csv', 'xlsx'])
        self.filesystem_go= pn.widgets.Button(name= 'GO!', button_type='primary', sizing_mode= 'stretch_width')
        filesystem_bunch= pn.Column(self.file_input, self.format, self.sheet_name, self.separator, self.filesystem_go, sizing_mode= 'stretch_width')
        self.file_input.param.watch(lambda event: self.__adjust_format(event), 'filename')

        # Step 3.2:
        filesystem_init_connection_parameters= []
        filesystem_connect_parameters = [self.file_input, self.format, self.sheet_name, self.separator]
        filesystem_get_schema_parameters = []
        filesystem_import_data_parameters = [self.datetime_column_selector, self.value_selector, self.catch_value]

        # Step 3.3:
        self.filesystem_go.on_click(lambda event: self.__combined_connector(SystemFiles.Connection, filesystem_init_connection_parameters, filesystem_connect_parameters, filesystem_get_schema_parameters, filesystem_import_data_parameters, self.filesystem_go))


        # Showcasing your custom widgets to panel sidebar. Add your widget bunch with the display name as a tuple. eg: ('Display Name': widget_bunch)
        # Step 3.4
        accordion= pn.Accordion(
                                ('SQL Database', database_bunch),
                                ('Apache Kafka', kafka_bunch),
                                ('URL', url_bunch),
                                ('System Files', filesystem_bunch),
                                #=============ADD HERE:================


                                #======================================
                                sizing_mode= 'stretch_width'
                                )
        
        # -------------------------------------------------------------------------------------------------------------------------------------------------
        #                                                            CHANGE TILL HERE
        # -------------------------------------------------------------------------------------------------------------------------------------------------

        # Making a clear button
        self.clear= pn.widgets.Button(name= 'CLEAR', button_type='danger', sizing_mode= 'stretch_width')

        # Making a STOP button
        self.stop=pn.widgets.Toggle(name='STOP', button_type='danger', sizing_mode='stretch_width', value=False)

        # Making a pause button
        self.playpause= pn.widgets.Button(name='Pause', button_type= 'warning', sizing_mode='stretch_width')
        self.playpause.on_click(self.__playpause)

        # Now finally making a sidebar
        self.sidebar= pn.Column(
                                    self.config_widgetbox,
                                    accordion,
                                    pn.Row(self.playpause, self.stop, self.clear)
                                )

    # =======================================================================================================================================================
    #                                                            Now defining watcher functions
    #                                                         Add your own watcher functions here
    # =======================================================================================================================================================

        

    def __playpause(self):
        if self.playpause.clicks%2 ==1:
            self.playpause.name='Play!'
            self.playpause.button_type='success'
        else:
            self.playpause.name='Pause'
            self.playpause.button_type='warning'


    def __change_button_color(widget):
        widget.button_type= 'danger'

    def catch_value(self):
        if self.data is None:
            self.data= pd.DataFrame()
        for mframe in self.consumer_object:
            self.data= pd.concat([self.data, mframe], ignore_index=True)
            self.gauge_callback()
            self.dfstream.send(mframe)
            print(self.stop.value)
            if self.stop.value:
                return
            if self.playpause.clicks % 2 == 1:
                while self.playpause.clicks % 2 != 1:
                    pass
        # return (not self.stop.value)

        # self.update_dashboard()

    def __init_connection(self, button, connection, params):
        button.button_type= 'success'
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
        self.connection= connection(*[param.value for param in params])

    def __connect(self, params):
        self.connect_status= self.connection.connect(*[param.value for param in params])


    def __get_schema(self, params):
        self.get_schema_status, schema= self.connection.get_schema(*[param.value for param in params])
        return schema
    
    def __display_modal(self, schema, import_data_params):
        print(schema)
        self.datetime_column_selector.options= schema
        self.value_selector.options= schema
        
        start_importing= pn.widgets.Button(name= 'GO', button_type= 'primary')
        start_importing.on_click(lambda event: self.__begin_showcase(import_data_params))
        self.template.modal[0].append(pn.Column(pn.Row(self.datetime_column_selector, self.value_selector), start_importing))
        
    def __combined_connector(self, connection, init_params, connect_params, get_schema_params, import_data_params, button):

        self.__init_connection(button, connection, init_params)

        self.__connect(connect_params)
        if self.connect_status:
            self.template.modal[0].append(pn.pane.Alert('Connection established!', alert_type= 'success'))
        else:
            self.template.modal[0].append(pn.pane.Alert('Failed to establish connection! Check Logs for details.', alert_type= 'danger'))
            time.sleep(2)
            self.connection.shutdown()
            self.template.close_modal()
            return
        
        schema= self.__get_schema(get_schema_params)
        if self.get_schema_status:
            self.template.modal[0].append(pn.pane.Alert('Schema Fetched!', alert_type= 'success'))
            self.__display_modal(schema, import_data_params)
        else:
            self.template.modal[0].append(pn.pane.Alert(schema, alert_type= 'danger'))
            self.connection.shutdown()
            time.sleep(4)
            self.template.close_modal()
            return
        
    def __begin_showcase(self, import_data_params):
        print([param.value if hasattr(param, 'value') else param for param in import_data_params])
        try:
            self.consumer_object= self.connection.import_data(*[param.value if hasattr(param, 'value') else param for param in import_data_params])
            self.template.modal[0].append(pn.pane.Alert('Successfully Imported Data!', alert_type='success'))
            self.connection.shutdown()
            self.connection_status.value= False
            self.catch_value()

        except Exception as e:
            print(e)
            self.template.modal[0].append(pn.pane.Alert('Import Unsuccessful! {}'.format(e), alert_type='danger'))
            self.connection.shutdown()
            time.sleep(2)
            self.template.close_modal()
            return
        
        self.__model_data()
        
    def __model_data(self):
        self.modelling_status.value= True
        modelling_update= pn.pane.Alert('Modelling Data Now!', alert_type='info')
        self.data= self.data.dropna()
        self.template.modal[0].append(pn.Row(self.modelling_status, modelling_update))

        # Exceptions with datetime conversion
        try:
            self.data['DATETIME'] = pd.to_datetime(self.data['DATETIME'])
            
        except Exception:
            modelling_update= pn.pane.Alert('DATETIME COLUMN FORMAT ERROR.', alert_type='danger')
            self.modelling_status.value= False
            self.template.modal[0].pop(-1)
            self.template.modal[0].append(pn.Row(self.modelling_status, modelling_update))
            return
        
        # Exceptions with value column to float conversion
        self.data['value'] = pd.to_numeric(self.data['value'], errors='coerce')
        self.data= self.data.dropna()
        if self.data.shape[0] == 0:
            modelling_update= pn.pane.Alert('value COLUMN FORMAT ERROR: No Relevant data found.', alert_type='danger')
            self.modelling_status.value= False
            self.template.modal[0].pop(-1)
            self.template.modal[0].append(pn.Row(self.modelling_status, modelling_update))
            return

        X= self.data[['DATETIME']]
        y=self.data['value']
        y_train, y_test, X_train, X_test = model_selection.train_test_split(y, X, train_size=self.training_shape.value)
        date_feat = preprocessing.DateFeaturizer(
                                                    column_name="DATETIME", 
                                                    with_day_of_week=True,
                                                    with_day_of_month=True
                                                )
        n_diffs = arima.ndiffs(y_train, max_d=5)
        _, X_train_feats = date_feat.fit_transform(y_train, X_train)
        self.model = pipeline.Pipeline([
                                    ('DATETIME', date_feat),
                                    ('arima', arima.AutoARIMA(d=n_diffs,
                                                            trace=3,
                                                            stepwise=True,
                                                            suppress_warnings=True,
                                                            seasonal=False))
                                ])
        self.template.modal[0].pop(-1)
        modelling_update= pn.pane.Alert('Modelling Over!', alert_type='info')
        self.modelling_status.value= False
        self.template.modal[0].append(pn.Row(self.modelling_status, modelling_update))

    def __adjust_format(self, event):
        format__= event.new.split('.')[-1]
        self.format.value= format__

    def curve_update(self, data):
        curve = hv.Curve(data, kdims=['DATETIME'], vdims=['value']).opts(line_width=1, color='lightblue', width=1200, show_grid=True)
        points = hv.Points(data, kdims=['DATETIME', 'value'], vdims=['value']).opts(color='color', cmap='viridis', padding=0.1, width=1200, xaxis=None, yaxis=None, marker='o')
        return (curve * points).opts(
                                    opts.Points(line_color='blue', size=5, padding=0.1, xaxis=None, yaxis=None),
                                    opts.Curve(line_width=2, color='lightblue')
                                    )

    def hist_callback(self, data=None):
        # Convert 'DATETIME' column to datetime type
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        empty_bars = hv.Bars([(0, 0)], kdims=['DATE'], vdims=['value'])

        if data is None:
            return empty_bars 

        if data['DATETIME'].isna().any():
            return empty_bars 

        if len(data) == 0:
            return empty_bars 
        
        latest_timestamp = data['DATETIME'].max()

        if self.last_unit.value=='years':
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(days=365 * self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.year

        elif self.last_unit.value=='months':
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(days=30 * self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.month
        
        elif self.last_unit.value=='days':
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(days=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.day
        
        elif self.last_unit.value=='hours':
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(hours=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.hour
        
        elif self.last_unit.value=='minutes':
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(minutes=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.minute

        elif self.last_unit.value=='seconds':
            
            last_data = data[data['DATETIME'] > (latest_timestamp - pd.Timedelta(seconds=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.second

        
        mean_value = last_data.groupby('LAST')['value'].mean().reset_index()
        mean_value['LAST'] = mean_value['LAST'].astype('category')
        print(mean_value)
        curve = hv.Bars(mean_value, kdims=['LAST'], vdims=['value'])
        return curve
    


    def gauge_callback(self):
        max_= self.data['value'].max()
        min_= self.data['value'].min()
        if max_ == min_:
            max_ += 100
            min_ -= 100
        value= self.data.tail(1)['value'].values[0]
        self.gauge.bounds= (min_, max_)
        self.gauge.value= value

    
    def gradient_pie(self, data):
        empty_bars = hv.Bars([(0, 0)], kdims=['DATE'], vdims=['value'])
        value_new = data['value'].diff()

        # Check if value_new contains NaN or other non-numeric values
        value_new= value_new.dropna()
        if value_new.isna().any():
            return empty_bars
        

        change= pd.DataFrame()
        change.loc['increase', 'shape']= value_new[value_new > 0].shape[0]
        change.loc['decrease', 'shape'] = value_new[value_new < 0].shape[0]
        change.loc['equal', 'shape'] = value_new[value_new == 0].shape[0]

        change= change.reset_index()

        # Create a Bars element with a 'color' dimension
        bars = hv.Bars(change, kdims=['index'], vdims=['shape'])
        

        return bars



    def boxplot(self, data):
        box= hv.BoxWhisker(data['value'], vdims='value')
        return box

