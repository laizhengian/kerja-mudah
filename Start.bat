@echo off
echo Starting Kerja Mudah...
python main.py
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not found.
    echo Please install Python 3.10 or higher from https://python.org
    echo.
    pause
)
