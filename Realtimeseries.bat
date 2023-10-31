@echo off
cd /d %~dp0
set log_file=log.txt

:: Set the name for the conda environment
set conda_env_name=PGh_Realtimeseries

:: Activate the conda environment
call conda activate PGh_Realtimeseries

(
    :: Check if the conda environment exists
    conda info --envs | findstr /i "\<PGh_Realtimeseries\>" > nul
    if %errorlevel% neq 0 (
        :: Create a new conda environment with Python 3.8
        conda create --name %conda_env_name% python=3.8 -y >> %log_file% 2>&1
        
        :: Install dependencies from requirements.txt if not already installed
        conda activate PGh_Realtimeseries
        conda update pip
        pip install -r requirements.txt >> %log_file% 2>&1
    )

    :: Activate the conda environment again to ensure we are working within it
    conda activate PGh_Realtimeseries

    :: Run your Python application (app.py)
    python app.py >> %log_file% 2>&1

    :: Exit the conda environment when done (optional)
    conda deactivate >> %log_file% 2>&1

    :: Display a completion message
    echo Installation and execution complete. You can now close this window.
)

:: Deactivate the conda environment if it's still active
call conda deactivate >> %log_file% 2>&1