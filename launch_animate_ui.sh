#!/bin/bash
# Wan2.2-Animate UI Launcher

echo "=========================================="
echo "   Wan2.2-Animate Character Replacement"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null
then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if app_animate.py exists
if [ ! -f "app_animate.py" ]; then
    echo "Error: app_animate.py not found in current directory"
    exit 1
fi

# Check if gradio is installed
python -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Gradio not found. Installing dependencies..."
    pip install -r requirements_ui.txt
fi

echo ""
echo "Starting Wan2.2-Animate Web UI..."
echo "The interface will open at http://localhost:7861"
echo ""
echo "This UI is for CHARACTER ANIMATION & REPLACEMENT"
echo "- Animation Mode: Character performs motions from video"
echo "- Replacement Mode: Replace character in video"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app_animate.py
