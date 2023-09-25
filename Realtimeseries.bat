@echo off
cd /d %~dp0
set log_file=log.txt

(
    :: Set the name for the conda environment
    set conda_env_name=RealTimeSeries

    :: Check if the conda environment exists
    conda env list | findstr /i "\<%conda_env_name%\>" > nul
    if %errorlevel% neq 0 (
        :: Create a new conda environment with Python 3.8
        conda create -n %conda_env_name% python=3.8 -y
    ) > %log_file% 2>&1

    :: Activate the conda environment
    conda activate %conda_env_name% >> %log_file% 2>&1

    :: Install dependencies from requirements.txt if not already installed
    pip list | findstr /i /g:requirements.txt > nul
    if %errorlevel% neq 0 (
        pip install -r requirements.txt >> %log_file% 2>&1
    )

    :: Run your Python application (app.py)
    python app.py >> %log_file% 2>&1

    :: Exit the conda environment when done (optional)
    conda deactivate >> %log_file% 2>&1

    :: Display a completion message
    echo Installation and execution complete. You can now close this window.
)