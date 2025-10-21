#!/bin/bash
# Wan2.2 UI Launcher

echo "======================================"
echo "   Wan2.2 Video Generator Web UI"
echo "======================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null
then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found in current directory"
    exit 1
fi

# Check if gradio is installed
python -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Gradio not found. Installing dependencies..."
    pip install -r requirements_ui.txt
fi

echo ""
echo "Starting Wan2.2 Web UI..."
echo "The interface will open at http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
