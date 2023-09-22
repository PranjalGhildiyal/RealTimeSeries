from RealTimeSeries.src.Components.ConnectionWidgets import ConnectionWidgets
import panel as pn
import pandas as pd
from holoviews.streams import Pipe, Buffer
import holoviews as hv
from bokeh.themes import built_in_themes
from holoviews import opts

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
        self.dfstream = Buffer(example, length=self.n_indexes.value, index=False)
        curve_dmap = hv.DynamicMap(hv.Curve, streams=[self.dfstream])
        point_dmap = hv.DynamicMap(hv.Points, streams=[self.dfstream])
        histogram_dmap= hv.DynamicMap(self.hist_callback, streams=[self.dfstream])
        hist_dmap= hv.DynamicMap(self.gradient_pie, streams=[self.dfstream])
        box_dmap= hv.DynamicMap(self.boxplot, streams=[self.dfstream])
        print('Done till here!')

        # Setting options:
        curve_dmap.opts(shared_axes=False)
        point_dmap.opts(shared_axes=False)
        histogram_dmap.opts(shared_axes=False)
        hist_dmap.opts(shared_axes=False)
        box_dmap.opts(shared_axes=False)
        lower_dashboard= (curve_dmap * point_dmap)
        lower_dashboard.opts(
                            opts.Points(color='count', line_color='blue', size=10, padding=0.1, xaxis=None, yaxis=None),
                            opts.Curve(line_width=5, color='blue')
                            )
        
        # Setting options:
        layout = hv.Layout(lower_dashboard).opts(
                                                sizing_mode='stretch_width'
                                            )

        main_dashboard= pn.GridSpec(sizing_mode='stretch_width')

        main_dashboard[0, 0]= self.gauge
        main_dashboard[0, 1] = histogram_dmap
        main_dashboard[0, 2]= hist_dmap
        main_dashboard[0, 3] = box_dmap
        main_dashboard[1, :] = layout


        self.template.main.append(main_dashboard)
        # Serving the app
        pn.serve(self.template)