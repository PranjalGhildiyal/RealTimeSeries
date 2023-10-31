from RealTimeSeriesDev.src.Components.ConnectionWidgets import ConnectionWidgets
import panel as pn
import pandas as pd
import holoviews as hv
from bokeh.themes import built_in_themes
from holoviews import opts
import warnings
warnings.filterwarnings('ignore')

class Dashboard(ConnectionWidgets):
    def __init__(self):
        super().__init__() 
        print('in Dashboard')
        hv.extension('bokeh')
        pn.extension('plotly', nthreads=0)
        theme = built_in_themes["dark_minimal"]
        hv.renderer('bokeh').theme = theme

        # Template decision
        self.template = pn.template.BootstrapTemplate(
                                                        title="Clinician",
                                                        sidebar=self.sidebar,
                                                        theme= 'dark'
                                                    )
        # Adding an empty column here. Necessary for design.
        self.template.modal.append(pn.Column())

        # opts.defaults(
        #                 opts.Curve(sizing_mode='stretch_both'),
        #                 opts.BoxWhisker(sizing_mode= 'stretch_both'),
        #                 opts.Bars(sizing_mode= 'stretch_both')
        #             )

        # Adding components for main here
        actual_stream= hv.DynamicMap(self.actual_update, streams=[self.dfstream])
        pred_stream= hv.DynamicMap(self.predicted_update, streams= [self.predstream])
        forecast_stream= hv.DynamicMap(self.forecasts_update, streams=[self.forecaststream]).opts(axiswise=True)

        lower_dashboard_dmap = pn.panel((actual_stream * pred_stream).opts(axiswise=True), sizing_mode='stretch_both')
        histogram_dmap= pn.panel(hv.DynamicMap(self.hist_callback, streams=[self.dfstream]).opts(shared_axes=False, axiswise=True),sizing_mode='stretch_both')
        hist_dmap= pn.panel(hv.DynamicMap(self.gradient_pie, streams=[self.dfstream]).opts(shared_axes=False, axiswise=True),sizing_mode='stretch_both')
        box_dmap= pn.panel(hv.DynamicMap(self.boxplot, streams=[self.dfstream]).opts(shared_axes=False, axiswise=True),sizing_mode='stretch_both')
        print('Done till here!')

        # Making a new lower-dashboard
        

        main_dashboard= pn.GridSpec(min_width= 800, min_height= 600, sizing_mode='scale_both')

        main_dashboard[0, 0]= self.gauge
        main_dashboard[0, 1:4]= histogram_dmap
        main_dashboard[0, 4]= hist_dmap
        main_dashboard[1, 0]= box_dmap
        main_dashboard[1, 1:4]= lower_dashboard_dmap
        main_dashboard[1, 4] = forecast_stream


        self.template.main.append(main_dashboard)
        # Serving the app
        pn.serve(self.template)