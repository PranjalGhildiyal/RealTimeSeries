# RealTimeSeries
Real time streaming of a time series with corresponding forecasts.

## Overview

RealTimeSeries is a powerful and flexible application designed for real-time time series data visualization and monitoring. It allows users to connect to various data sources, including databases, Apache Kafka, URLs, and the local filesystem, to visualize time series data in a dynamic and interactive dashboard. This project is particularly well-suited for applications involving real-time data simulation and monitoring.

![Dashboard](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/attachments/dashboardFirstLooks.gif)

### Key Features

- **Flexible Data Sources**: RealTimeSeries supports a variety of data sources out of the box, including databases, Apache Kafka, URLs, and the filesystem. Additionally, it can be easily extended to support custom data import options.

- **Real-Time Visualization**: The application provides real-time visualization of time series data, making it ideal for monitoring applications where data is continuously updated.

- **Advanced Plotting**: RealTimeSeries offers features such as box plots, aggregate plots, and change bar plots that update in real time, providing deeper insights into time series data.

- **Scalability**: Users can import and simulate data independently, allowing for a scalable and versatile data analysis environment.
  
- **Forecasting and Real-Time Predictions** (Upcoming): Future updates will incorporate forecasting techniques for real-time predictions, enhancing the application's capabilities.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Connecting to Data Sources](#connecting-to-data-sources)
  - [Customizing Data Import](#customizing-data-import)
  - [Real-Time Visualization](#real-time-visualization)
- [Contributing](#contributing)
- [License](#license)
- [Future Ahead](#future-ahead)

## Getting Started

### Prerequisites

Before you begin, ensure that you have the following prerequisites installed on your system:

- [Python](https://www.python.org/) (version 3.8)
- [Conda](https://conda.io/) (for managing the Conda environment)
- [Zookeeper](https://zookeeper.apache.org/) (only if a Kafka topic needs to be streamed)
- [ApacheKafka](https://kafka.apache.org/)

### Installation

1. Clone the RealTimeSeries repository to your local machine:

   ```bash
   git clone https://github.com/your-username/RealTimeSeries.git
   ```
2. Navigate to the project directory:
   ```bash
   cd RealTimeSeries
   ```
3. Run the provided batch script to set up the Conda environment and start the application:
   ```bash
   Realtimeseries.sh
   ```
This script will create a Conda environment named "RealTimeSeries," install the required dependencies, and launch the RealTimeSeries application.

## Usage

### Connecting to Data Sources

RealTimeSeries supports various data sources for time series data:

- **Database**: Connect to a database to retrieve time series data.
- **Apache Kafka**: Stream time series data from an Apache Kafka cluster.
- **URL**: Fetch time series data from a remote URL.
- **Filesystem**: Read time series data from local files.

![ImportExample](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/attachments/dataImport.gif)

The application provides a user-friendly interface for configuring these connections. Follow the prompts to specify your connection details.

### Customizing Data Import

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

------------------------------------------------------------------------------------------------------------------------------------

### Real-Time Visualization

Once you have configured your data source, RealTimeSeries will continuously visualize the time series data in real time. The dynamic dashboard allows you to monitor and interact with the data as it updates.
![Visualization](https://github.com/PranjalGhildiyal/RealTimeSeries/blob/production/attachments/startSimulation.gif)

## Contributing

We welcome contributions to RealTimeSeries. If you'd like to contribute, please follow our Contribution Guidelines for detailed instructions on how to get started.

## License
This project is licensed under the [MIT](https://opensource.org/license/mit/) License. You are free to use, modify, and distribute this software as specified in the license.

## Future Ahead

We have exciting plans for the future of RealTimeSeries. Here's a glimpse of what's coming:

- **Forecasting Techniques**: We are working on incorporating advanced forecasting techniques to enable real-time predictions of time series data.

Stay tuned for updates and enhancements to make RealTimeSeries even more powerful and versatile!

---

