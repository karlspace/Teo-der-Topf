#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Enhanced startup script with virtual environment support
# For modern deployment, consider using: systemctl start teo-der-topf

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$DIR/venv"

# Check if systemd service is running
if systemctl is-active --quiet teo-der-topf 2>/dev/null; then
    echo "Teo der Topf is running as a system service."
    echo "To stop: sudo systemctl stop teo-der-topf"
    echo "To view logs: sudo journalctl -u teo-der-topf -f"
    echo "To restart: sudo systemctl restart teo-der-topf"
    exit 1
fi

# Check if the application is already running manually
if pgrep -f "python.*main.py" > /dev/null; then
    echo "The Python Console Application is already running!"
    echo "Run stop_app.sh to stop the running process."
    exit 1
fi

echo "=== Teo der Topf Manual Startup ==="

# Setup virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR" --system-site-packages
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install all Requirements if needed
if [ -f "$DIR/requirements.txt" ] && [ ! -f "$DIR/.python-packages-ready" ]; then
    echo "Installing Python Requirements..."
    pip install --upgrade pip
    pip install -r "$DIR/requirements.txt"
    echo "$(date): Python environment setup completed" > "$DIR/.python-packages-ready"
    echo "Python requirements installed successfully"
elif [ -f "$DIR/requirements.txt" ]; then
    echo "Checking for requirement updates..."
    pip install --upgrade -r "$DIR/requirements.txt" || true
fi

# Show system info
echo "--- System Information ---"
echo "Python: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"
echo "Working directory: $(pwd)"

# Check hardware
echo "--- Hardware Check ---"
if [ -c /dev/spidev0.0 ]; then
    echo "SPI: Available"
else
    echo "SPI: Not available (check config.txt and reboot)"
fi

if [ -c /dev/i2c-1 ]; then
    echo "I2C: Available"
else
    echo "I2C: Not available (check config.txt and reboot)"
fi

# Start Application
echo "--- Starting Application ---"
echo "Press Ctrl+C to stop"
echo ""
cd "$DIR"
python3 ./main.py
