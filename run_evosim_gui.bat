@echo off
REM EvoSim GUI Launcher for Windows
REM This batch file launches the EvoSim GUI application from the project root

echo EvoSim GUI Launcher
echo ==================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Run the GUI
echo Starting EvoSim GUI...
python run_evosim_gui.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo GUI exited with an error. Press any key to close.
    pause
)
