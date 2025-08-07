#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Enhanced startup script for Teo der Topf with virtual environment support

set -e

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$DIR/venv"
PYTHON_READY_MARKER="$DIR/.python-env-ready"

echo "=== Teo der Topf Startup ==="
echo "Working directory: $DIR"

# Create and setup virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR" --system-site-packages
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install/upgrade pip and requirements if needed
if [ -f "$DIR/requirements.txt" ] && [ ! -f "$PYTHON_READY_MARKER" ]; then
    echo "Installing/updating Python requirements..."
    pip install --upgrade pip
    pip install -r "$DIR/requirements.txt"
    echo "$(date): Python environment setup completed" > "$PYTHON_READY_MARKER"
    echo "Python requirements installed successfully"
elif [ -f "$DIR/requirements.txt" ]; then
    echo "Checking for requirement updates..."
    pip install --upgrade -r "$DIR/requirements.txt" || true
fi

# Check if the application is already running (for manual starts)
if pgrep -f "python.*main.py" > /dev/null; then
    echo "WARNING: Teo der Topf is already running!"
    echo "To stop the running instance, use: sudo systemctl stop teo-der-topf"
    echo "Or run: ./stop_app.sh"
    exit 1
fi

# Display system information
echo "--- System Information ---"
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"
echo "Working directory: $(pwd)"
echo "User: $(whoami)"
echo "Groups: $(groups)"

# Check hardware interfaces
echo "--- Hardware Status ---"
if [ -c /dev/spidev0.0 ]; then
    echo "SPI: ✓ Available"
else
    echo "SPI: ✗ Not available (check config.txt)"
fi

if [ -c /dev/i2c-1 ]; then
    echo "I2C: ✓ Available"
else
    echo "I2C: ✗ Not available (check config.txt)"
fi

# Start the application
echo "--- Starting Teo der Topf ---"
echo "Press Ctrl+C to stop the application"
echo ""

cd "$DIR"
exec python main.py