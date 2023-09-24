@echo off

:: Set the name for the conda environment
set conda_env_name=RealTimeSeries

:: Check if the conda environment exists
conda env list | findstr /i "\<%conda_env_name%\>" > nul
if %errorlevel% neq 0 (
    :: Create a new conda environment with Python 3.8
    conda create -n %conda_env_name% python=3.8 -y
)

:: Activate the conda environment
conda activate %conda_env_name%

:: Install dependencies from requirements.txt if not already installed
pip list | findstr /i /g:requirements.txt > nul
if %errorlevel% neq 0 (
    pip install -r requirements.txt
)

:: Run your Python application (app.py)
panel serve app.py --show --autoreload

:: Exit the conda environment when done (optional)
conda deactivate

:: Display a completion message
echo Installation and execution complete. You can now close this window.