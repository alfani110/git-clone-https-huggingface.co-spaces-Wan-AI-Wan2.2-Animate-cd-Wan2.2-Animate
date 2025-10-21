@echo off
REM Wan2.2 UI Launcher for Windows

echo ======================================
echo    Wan2.2 Video Generator Web UI
echo ======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo Error: app.py not found in current directory
    pause
    exit /b 1
)

REM Check if gradio is installed
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo Gradio not found. Installing dependencies...
    pip install -r requirements_ui.txt
)

echo.
echo Starting Wan2.2 Web UI...
echo The interface will open at http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
