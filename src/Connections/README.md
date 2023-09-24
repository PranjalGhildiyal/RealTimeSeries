# Customizing Data Import

RealTimeSeries is designed to be highly customizable. If you need to connect to a data source that is not included in the predefined options, you can extend the application to support custom data import methods. Detailed instructions:

#### ``Step 3.1``: Define Buttons for Input to a Connector
   - Go to [ConnectionWidgets.py](src/Components/ConnectionWidgets.py). You need to make changes there in order to build a custom import method.
   - Structure of the Connector:
       - The connector should be a python class, stored in [`Connections`](src/Connections) folder in the src folder.
       - The connector should have four attributes:
           - `__init__(*init_connection_parameters)`: The `__init__` function.
           - `connect(*connect_parameters)`: The method to connect. This should return a boolean `True` or `False` based on the connection status.
           - `get_schema(*get_schema_parameters)`: Returns a tuple containing:
               1. `status`(bool)
               2. `column_names`(list)
           - `import_data(*import_data_parameters)`: return a generator object for the data.
       - Don't forget to wrap all the relevant widgets in a widget bunch, which will be used later.


#### ``Step 3.2``: Define Input Parameter List for Each Step of the Connector

   - The input parameters are Holoviz Panel widgets with the `value` attribute as parameters OR any other entity not having a `value` attribute.


#### ``Step 3.3``: Add Watcher Function in the Syntax

   - Add a watcher function in the syntax:
   
   ```python
   self.your_custom_import_button_widget.on_click(lambda event: self.__combined_connector(
       Method.Connection,
       init_param_list,
       connect_param_list,
       get_schema_param_list,
       import_data_param_list,
       self.your_custom_import_button_widget
   ))
```


#### ``Step 3.4``: Add Your Widget Bunch to the Accordion

   - Add your widget bunch to the accordion as a tuple, with the first element as the display name. For example:
   
   ```python
   ('Display Name', widget_bunch)
   ```


**PLEASE SEE [ConnectionWidgets.py](src/Components/ConnectionWidgets.py) FOR FURTHER DETAILS**