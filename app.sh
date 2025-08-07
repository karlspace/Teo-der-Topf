#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Get the directory of the current script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install all Requirements on Start of the Image, if required (RUN TIME)
if [ -f "$DIR/requirements.txt" ] && [ ! -f "$DIR/.python-packages-ready" ]; then
  echo "Installing Python Requirements..."
  pip install --break-system-packages -r "$DIR/requirements.txt"
  echo "TO RUN PIP INSTALL FOR REQUIREMENTS.TXT ON NEXT START. DELETE THIS FILE." > "$DIR/.python-packages-ready"
fi


# Check if the application is already running
if pgrep -f main.py > /dev/null
then
    echo "The Python Console Application is already running!"
    echo "Run stop_app.sh to stop the running process."
else
    # Start Application
    echo "Starting Python Console Application..."
    cd "$DIR"
    python3 ./main.py
fi
