from RealTimeSeries.src.Components.ConnectionWidgets import ConnectionWidgets
import panel as pn
import pandas as pd
from holoviews.streams import Pipe, Buffer
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
        pn.extension('plotly')
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

        # Adding components for main here
        example = pd.DataFrame({'DATETIME': [], 'value': []}, columns=['DATETIME', 'value'])
        self.dfstream = Buffer(example, length=self.n_indexes.value, index=False)
        lower_dashboard_dmap = hv.DynamicMap(self.curve_update, streams=[self.dfstream])
        histogram_dmap= hv.DynamicMap(self.hist_callback, streams=[self.dfstream])
        hist_dmap= hv.DynamicMap(self.gradient_pie, streams=[self.dfstream])
        box_dmap= hv.DynamicMap(self.boxplot, streams=[self.dfstream])
        print('Done till here!')

        # Setting options:
        histogram_dmap.opts(shared_axes=False)
        hist_dmap.opts(shared_axes=False)
        box_dmap.opts(shared_axes=False)

        main_dashboard= pn.GridSpec(sizing_mode='stretch_width')

        main_dashboard[0, 0]= self.gauge
        main_dashboard[0, 1] = histogram_dmap
        main_dashboard[0, 2]= hist_dmap
        main_dashboard[0, 3] = box_dmap
        main_dashboard[1, :] = lower_dashboard_dmap


        self.template.main.append(main_dashboard)
        # Serving the app
        pn.serve(self.template)