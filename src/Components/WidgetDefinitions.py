from RealTimeSeries.src.Components.ConfigReader import ConfigReader
import panel as pn
import threading
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
        
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

        self.last_n= pn.widgets.IntInput(name='Enter `n` for metrics', value=20, sizing_mode= 'stretch_width')
        self.last_unit= pn.widgets.Select(name= 'Select unit', options= ['minutes', 'hours', 'seconds', 'days', 'months', 'years'], value='hours', sizing_mode= 'stretch_width')
        self.n_indexes= pn.widgets.IntInput(name='Enter number of observations to display', sizing_mode= 'stretch_width', value= 100)
        self.feature_shape= pn.widgets.IntInput(name= 'Enter forecast shape', sizing_mode='stretch_width', value=20)
        self.training_shape= pn.widgets.IntInput(name='Enter minimum training threshold', sizing_mode= 'stretch_width', value=10000)
        self.config_widgetbox= pn.WidgetBox(pn.Column(pn.Row(self.last_n, self.last_unit), pn.Row(self.feature_shape, self.n_indexes), self.training_shape), sizing_mode= 'stretch_width')

        # Making main
        stops = [
                (0.0, '#28242c'),     # Dark blue at the lowest value
                (0.5, '#2596be'),
                (1.0, 'cyan') # Light blue at the highest value
            ]
        
        cmap = LinearSegmentedColormap.from_list('shades_of_blue', stops)
        colors = [(value/1000, plt.cm.colors.to_hex(cmap(value/1000))) for value in range(1000)]
        self.gauge= pn.indicators.Gauge(name='', value=0, format= '{value}', colors= colors, sizing_mode= 'stretch_both')# height= 300, wwidth= 300)
        self.bars= pn.pane.Plotly()
        self.pie_chart= pn.pane.Plotly()
        self.main_chart= pn.pane.Plotly()

        # Regarding multithreading
        self.stop_flag = threading.Event()
        
        # Defining data for the first time
        self.data= None
