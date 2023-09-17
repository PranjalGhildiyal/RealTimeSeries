from RealTimeSeries.src.Components.ConfigReader import ConfigReader
import panel as pn    
        
#===========================================================
#                         Step 2
#============================================================
# Defining all the important widgets for the app here.
        
class WidgetDefinitions(ConfigReader):
    def __init__(self): 
        super().__init__()
        print('in WidgetDefinitions')

        # Defining important widgets
        self.datetime_column_selector= pn.widgets.Select(name= 'Select datetime column')
        self.value_selector= pn.widgets.Select(name= 'Select value column')
        self.connection_status= pn.indicators.LoadingSpinner(value=False, color='primary', bgcolor='dark')
        self.modelling_status= pn.indicators.LoadingSpinner(value=False, color='primary', bgcolor='dark', size= 50)

        # Defining connection status
        self.connection_init= False
        self.connect_status= False
        self.get_schema_status= False
        self.import_data_status= False

        self.last_n= pn.widgets.IntInput(name='Enter `n` for metrics', value=1, sizing_mode= 'stretch_width')
        self.last_unit= pn.widgets.Select(name= 'Select unit', options= ['minutes', 'hours', 'seconds', 'days', 'months', 'years'], value='minutes', sizing_mode= 'stretch_width')
        self.n_indexes= pn.widgets.IntInput(name='Enter number of observations to display', sizing_mode= 'stretch_width', value= 100)
        self.feature_shape= pn.widgets.IntInput(name= 'Enter forecast shape', sizing_mode='stretch_width', value=20)
        self.training_shape= pn.widgets.FloatInput(name='Enter training ratio', sizing_mode= 'stretch_width', value=0.8)
        self.config_widgetbox= pn.WidgetBox(pn.Column(pn.Row(self.last_n, self.last_unit), pn.Row(self.feature_shape, self.n_indexes), self.training_shape), sizing_mode= 'stretch_width')

        # Making main
        self.gauge= pn.indicators.Gauge(name='Failure Rate', value=10, format= '{value}')
        self.bars= pn.pane.Plotly()
        self.pie_chart= pn.pane.Plotly()