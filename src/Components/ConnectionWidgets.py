# Import your custom connector
from RealTimeSeriesDev.src.Components.WidgetDefinitions import WidgetDefinitions
from RealTimeSeriesDev.src.Connections import DataBase, Kafka, SystemFiles, url
from RealTimeSeriesDev.src.CustomModels.Model import ModelDetails
import panel as pn
import time
import holoviews as hv
import pandas as pd
from pmdarima import arima
from pmdarima import model_selection
from pmdarima import pipeline
from pmdarima import preprocessing
from holoviews import opts
import threading
import asyncio


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
        self.clear.on_click(self.__CLEAR)

        # Making a STOP button
        self.stop=pn.widgets.Button(name='STOP', button_type='danger', sizing_mode='stretch_width')
        self.stop.on_click(self.__STOP)

        # # Making a pause button
        # self.playpause= pn.widgets.Button(name='Pause', button_type= 'warning', sizing_mode='stretch_width')
        # self.playpause.on_click(self.__playpause)

        # Making the modelling widget:
        self.model_selector= pn.widgets.Select(name='Select Model Type', options= [None] + self.inquiry.available_models, value=None)
        self.modelling_indicator= pn.widgets.Button(name='Model Data', button_type= 'light', button_style='outline', sizing_mode= 'stretch_both')
        # self.modelling_indicator.param.watch(lambda event: self.__change_button_color(self.modelling_indicator, button_type='success', button_style=None), 'value')
        self.modelling_indicator.param.watch(lambda event: self.model_data_trigger(), 'value')

        widgetbox= pn.WidgetBox(pn.Column(pn.Row(self.model_selector, self.modelling_indicator)), sizing_mode= 'stretch_width')
        # Now finally making a sidebar
        self.sidebar= pn.Column(
                                    self.config_widgetbox,
                                    widgetbox,
                                    accordion,
                                    pn.Row(self.stop, self.clear),
                                    sizing_mode='stretch_width'
                                )

    # =======================================================================================================================================================
    #                                                            Now defining watcher functions
    #                                                         Add your own watcher functions below
    # =======================================================================================================================================================

    def __STOP(self, event=None):
        self.stop_flag.set()
        print('STOPPED!')
        

    def __CLEAR(self, event=None):
        self.dfstream.clear()
        self.predstream.clear()
        self.gauge.bounds= (0, 100)
        self.gauge.value= 50
        self.data= None
    
    def model_data_trigger(self):
        self.modelling_thread= threading.Thread(target=self.__model_data)
        self.modelling_thread.daemon = True
        self.modelling_thread.start()



    def __change_button_color(self, widget, button_type=None, button_style=None):
        if button_type is None:
            button_type=widget.button_type
        if button_style is None:
            button_style=widget.button_style
        
        widget.button_type= button_type
        widget.button_style= button_style

    def catch_value(self):
        if self.data is None:
            self.data= pd.DataFrame()
        for mframe in self.consumer_object:
            if self.stop_flag.is_set():
                break 
            self.data= pd.concat([self.data, mframe], ignore_index=True)
            
            time.sleep(0.1)

            if self.stop_flag.is_set():
                break 
            self.gauge_callback()
            if self.stop_flag.is_set():
                break 
            self.dfstream.send(mframe)
            if self.stop_flag.is_set():
                break 
            # Streaming predictions
            if self.modelled_yet:
                self.send_predictions(mframe)
            if self.stop_flag.is_set():
                break 

    
    def send_predictions(self, mframe):

        nth_step_prediction= self.model.predict(X=mframe[['DATETIME']], return_conf_int=True)
        pred= nth_step_prediction[0]
        range_min= nth_step_prediction[1][0][0]
        range_max= nth_step_prediction[1][0][1]
        pred_frame = pd.DataFrame({'DATETIME': list(mframe['DATETIME'].values)[0], 'value': pred, 'max': range_max, 'min': range_min})
        self.predstream.send(pred_frame)
        self.__update_model(mframe)
    
    def __update_model(self, mframe):
        self.model.update(mframe['value'], mframe[['DATETIME']])

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
        self.connection= connection(*[param.value if hasattr(param, 'value') else param for param in params])

    def __connect(self, params):
        self.connect_status= self.connection.connect(*[param.value if hasattr(param, 'value') else param for param in params])


    def __get_schema(self, params):
        self.get_schema_status, schema= self.connection.get_schema(*[param.value if hasattr(param, 'value') else param for param in params])
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
            self.stop_flag.clear()  # Ensure the flag is initially cleared
            self.loop_thread = threading.Thread(target=self.catch_value)
            self.loop_thread.daemon= True
            self.loop_thread.start()
            self.template.close_modal()
            # self.__model_data()

        except Exception as e:
            print(e)
            self.template.modal[0].append(pn.pane.Alert('Import Unsuccessful! {}'.format(e), alert_type='danger'))
            self.connection.shutdown()
            time.sleep(2)
            self.template.close_modal()
            return
        
        
        
    def __model_data(self):
        self.modelling_indicator.button_type='success'
        self.modelling_indicator.button_style= 'outline'

        self.template.modal[0].clear()
        print('Opening modal')
        self.template.open_modal()
        self.modelling_status.value= True
        self.template.modal[0].append(
                                        pn.Row(
                                                pn.layout.HSpacer(),
                                                self.modelling_status,
                                                pn.layout.HSpacer()
                                                )
                                        )

        modelling_update= pn.pane.Alert('Modelling Data Now!', alert_type='info', sizing_mode= 'stretch_width')
        self.template.modal[0].append(modelling_update)

        if self.data.shape[0] < self.training_shape.value:
            self.modelling_indicator.button_type='danger'
            self.modelling_indicator.button_style= 'outline'
            modelling_update= pn.pane.Alert('Insufficient number of datapoints. Either change the minimum required datapoints or try again later.')
            self.modelling_status.value= False
            self.template.modal[0].append(modelling_update)
            return
        
        # Exceptions with datetime conversion
        data= self.data
        try:
            data['DATETIME'] = pd.to_datetime(data['DATETIME'])
            
        except Exception:
            modelling_update= pn.pane.Alert('DATETIME COLUMN FORMAT ERROR.', alert_type='danger')
            self.modelling_status.value= False
            self.template.modal[0].append(modelling_update)
            return
        
        
        # Exceptions with value column to float conversion
        data['value'] = pd.to_numeric(data['value'], errors='coerce')
        data= data.dropna()
        if data.shape[0] == 0:
            modelling_update= pn.pane.Alert('value COLUMN FORMAT ERROR: No Relevant data found.', alert_type='danger')
            self.modelling_status.value= False
            self.template.modal[0].append(modelling_update)
            return

        X= data[['DATETIME']]
        y= data['value']


        model= ModelDetails(self.model_selector.value).model
        self.model_selector.value= None

        # date_feat = preprocessing.DateFeaturizer(
        #                                             column_name="DATETIME", 
        #                                             with_day_of_week=True,
        #                                             with_day_of_month=True
        #                                         )
        # n_diffs = arima.ndiffs(y, max_d=5)
        # model = pipeline.Pipeline([
        #                             ('DATETIME', date_feat),
        #                             ('arima', arima.AutoARIMA(d=n_diffs,
        #                                                     trace=3,
        #                                                     stepwise=True,
        #                                                     suppress_warnings=True,
        #                                                     seasonal=False))
        #                         ])
        
        model.fit(y, X)
        modelling_update= pn.pane.Alert('Modelling Over!', alert_type='info')
        self.modelling_status.value= False
        self.template.modal[0].append(modelling_update)
        
        print('Modelling complete!')
        self.model= model
        self.modelled_yet= True

    def __adjust_format(self, event):
        format__= event.new.split('.')[-1]
        self.format.value= format__

    def actual_update(self, data):
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        curve = hv.Curve(data, kdims=['DATETIME'], vdims=['value']).opts(line_width=1, color='lightblue', show_grid=True, responsive=True, gridstyle= {'grid_line_color': '#2596be'})#, width=1300, height= 700)
        return (curve).opts(
                            opts.Curve(line_width=2)
                            )
    
    def predicted_update(self, data):
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        curve = hv.Curve(data, kdims=['DATETIME'], vdims=['value']).opts(responsive=True, color='orange')#, width=1300, height= 700)
        area = hv.Area(data, vdims=['max', 'min'], kdims=['DATETIME']).opts(alpha=0.2, color='cyan')
        return (curve * area).opts(
                            opts.Curve(line_width=2)
                            )


    def hist_callback(self, data=None):
        # Convert 'DATETIME' column to datetime type

        if data is None:
            data = pd.DataFrame({'LAST': range(self.last_n.value), 'value': [0] * self.last_n})
            return hv.Bars(data, kdims=['LAST'], vdims=['value']).opts(responsive=True)

        if data['DATETIME'].isna().any():
            data = pd.DataFrame({'LAST': range(self.last_n.value), 'value': [0] * self.last_n.value})
            return hv.Bars(data, kdims=['LAST'], vdims=['value']).opts(responsive=True)
        
        if len(data) == 0:
            data = pd.DataFrame({'LAST': range(self.last_n.value), 'value': [0] * self.last_n.value})
            return hv.Bars(data, kdims=['LAST'], vdims=['value']).opts(responsive=True)
        
        data['DATETIME'] = pd.to_datetime(data['DATETIME'])
        
        # latest_timestamp = data['DATETIME'].max()

        if self.last_unit.value=='years':
            latest_timestamp = data['DATETIME'].max().year
            last_data = data[data['DATETIME'].dt.year > (latest_timestamp - self.last_n.value)]
            last_data['LAST']= last_data['DATETIME'].dt.year

        elif self.last_unit.value=='months':
            latest_timestamp = pd.Period(data['DATETIME'].max().to_period('M'), freq='M')
            last_data = data[data['DATETIME'].dt.to_period('M') > (latest_timestamp - self.last_n.value)]
            last_data['LAST']= last_data['DATETIME'].dt.to_period('M')
        
        elif self.last_unit.value=='days':
            latest_timestamp = data['DATETIME'].max().date()
            last_data = data[data['DATETIME'].dt.date > (latest_timestamp - pd.DateOffset(days= self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.date
        
        elif self.last_unit.value=='hours':
            latest_timestamp = data['DATETIME'].max().floor('H')
            last_data = data[data['DATETIME'].dt.floor('H') > (latest_timestamp - pd.DateOffset(hours=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.floor('H')
        
        elif self.last_unit.value=='minutes':
            latest_timestamp = data['DATETIME'].max().floor('T')
            last_data = data[data['DATETIME'].dt.floor('T')  > (latest_timestamp - pd.DateOffset(minutes=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.floor('T')

        elif self.last_unit.value=='seconds':
            latest_timestamp = data['DATETIME'].max().floor('S')
            last_data = data[data['DATETIME'].dt.floor('S')  > (latest_timestamp - pd.DateOffset(seconds=self.last_n.value))]
            last_data['LAST']= last_data['DATETIME'].dt.floor('S')

        
        mean_value = last_data.groupby('LAST')['value'].mean().reset_index()
        mean_value['LAST'] = mean_value['LAST'].astype('category')

        curve = hv.Bars(mean_value, kdims=['LAST'], vdims=['value']).opts(responsive=True, xticks={'rotation': 45})
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
        

        return bars.opts(responsive=True)#.opts(width= 200, height= 300)



    def boxplot(self, data):
        box= hv.BoxWhisker(data['value'], vdims='value')#.opts(width= 200, height= 700)
        return box.opts(responsive=True)

