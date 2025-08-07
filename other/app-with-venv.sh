#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a virtual environment if it doesn't exist
if [ ! -d "$DIR/venv" ]; then
  echo "Installing Python Virtual Environment..."
  python3 -m venv "$DIR/venv"
fi

# Activate the virtual environment on every startup
echo "Activating the Python Virtual Environment..."
source "$DIR/venv/bin/activate"

# Install all Requirements on Start of the Image, if required (RUN TIME)
if [ -f "$DIR/requirements.txt" ] && [ ! -f "$DIR/.python-packages-ready" ]; then
  echo "Installing Python Requirements..."
  pip install -r "$DIR/requirements.txt"
  echo "TO RUN PIP INSTALL FOR REQUIREMENTS.TXT ON NEXT START. DELETE THIS FILE." > "$DIR/.python-packages-ready"
fi

# Check if the application is already running
if pgrep -f main.py > /dev/null
then
    echo "The Python Console Application is already running!"
else
    # Start Application
    echo "Starting Python Console Application..."
    cd "$DIR"
    python3 ./main.py
fi
