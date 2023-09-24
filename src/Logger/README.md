### `Applogger` Class

Custom Logger class for RealTimeSeries App.

**Properties:**

- `logger`: Returns a logger initialized for a specific connection method. It can be used to log in the directory mentioned in [`config.ini`].

- `shutdown`: Shuts down the connection to prevent duplicate entries in the log file.