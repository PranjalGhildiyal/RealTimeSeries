from RealTimeSeries.src.Components.ConnectionWidgets import ConnectionWidgets
import panel as pn
import pandas as pd
from holoviews.streams import Pipe, Buffer
import holoviews as hv
from bokeh.themes import built_in_themes

hv.extension('bokeh')
theme = built_in_themes["dark_minimal"]
hv.renderer('bokeh').theme = theme


class Dashboard(ConnectionWidgets):
    def __init__(self):
        super().__init__() 
        print('in Dashboard')

        # Template decision
        self.template = pn.template.BootstrapTemplate(
                                                        title="Clinician",
                                                        sidebar=self.sidebar,
                                                        theme= 'dark'
                                                    )
        # Adding an empty column here. Necessary for design.
        self.template.modal.append(pn.Column())

        # Adding components for main here
        example = pd.DataFrame({'DATETIME': [], 'value': []}, columns=['DATETIME', 'value'])
        self.dfstream = Buffer(example, length=100, index=False)
        curve_dmap = hv.DynamicMap(hv.Curve, streams=[self.dfstream])
        point_dmap = hv.DynamicMap(hv.Points, streams=[self.dfstream])
        histogram_dmap= hv.DynamicMap(self.hist_callback, streams=[self.dfstream])
        gauge_dmap= hv.DynamicMap(self.gauge_callback, streams=[self.dfstream])
        hist_dmap= hv.DynamicMap(self.gradient_pie, streams=[self.dfstream])

        upper_dash= pn.Row(gauge_dmap, histogram_dmap, hist_dmap, sizing_mode= 'stretch_width')
        lower_dash= pn.Column(curve_dmap * point_dmap, sizing_mode= 'stretch_width')

        self.template.main.append(pn.Column(upper_dash, lower_dash, sizing_mode= 'stretch_width'))
        # Serving the app
        pn.serve(self.template)