#!/bin/bash

# Set the name for the conda environment
conda_env_name="RealTimeSeries"

# Check if the conda environment exists
if ! conda env list | grep -q $conda_env_name; then
    # Create a new conda environment with Python 3.8
    conda create -n $conda_env_name python=3.8 -y
fi

# Activate the conda environment
conda activate $conda_env_name

# Install dependencies from requirements.txt if not already installed
if ! pip list | grep -q -F -f requirements.txt; then
    pip install -r requirements.txt
fi

# Alternatively, you can use an environment.yml file if available
# conda env update -f environment.yml

# Run your Python application (app.py)
python app.py

# Make the run_app.sh script executable
chmod +x run_app.sh

echo "Installation complete. You can now run the application by executing Realtimeseries.sh."
