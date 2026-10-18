@echo off
cd /d "%~dp0"

echo Starting Titanic Survival Analysis project...

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found in PATH.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
python -m jupyter notebook Titanic_analysis.ipynb
