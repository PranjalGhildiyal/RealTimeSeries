from RealTimeSeries.src.Components.ConnectionWidgets import ConnectionWidgets
import panel as pn



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


        # Serving the app
        pn.serve(self.template)

        