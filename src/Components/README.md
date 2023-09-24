# Components

- To visualize, open `structure.drawio` on [draw.io](https://app.diagrams.net/)
- ConfigReader < WidgetDefinitions < ConnectionWidgets < App

    - [**ConfigReader**](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/src/Components/ConfigReader.py): Reads config file to import necessary default user information.
    
    - [**WidgetDefinitions**](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/src/Components/WidgetDefinitions.py): Defines basic widgets necessary for the app and places them in self.
    
    - [**ConnectionWidgets**](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/src/Components/ConnectionWidgets.py):
        
        - Here we import and use any custom import method defined by the user.
        
        - Also, here we define all the callback functions that would be required in this and other child class(es).
    
    - [**App**](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/src/Components/Dashboard.py):
        
        - Defines the final `App` class.
        
        - This is where the template is finally served.
        
        - All the plots and the `GridSpec` for the panel are created here. Any new plots would be attached here.
  
