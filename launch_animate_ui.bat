@echo off
REM Wan2.2-Animate UI Launcher for Windows

echo ==========================================
echo    Wan2.2-Animate Character Replacement
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if app_animate.py exists
if not exist "app_animate.py" (
    echo Error: app_animate.py not found in current directory
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
echo Starting Wan2.2-Animate Web UI...
echo The interface will open at http://localhost:7861
echo.
echo This UI is for CHARACTER ANIMATION ^& REPLACEMENT
echo - Animation Mode: Character performs motions from video
echo - Replacement Mode: Replace character in video
echo.
echo Press Ctrl+C to stop the server
echo.

python app_animate.py
pause
