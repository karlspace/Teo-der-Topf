#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Get the PID of the running process
PID=$(pgrep -f main.py)

# If the process is running, send it the SIGTERM signal
if [ -n "$PID" ]; then
    echo "Sending SIGTERM to process $PID..."
    kill -TERM $PID

    # Try to confirm process termination for up to 5 seconds
    for i in {1..5}
    do
        sleep 1
        if ! kill -0 $PID 2>/dev/null; then
            echo "The process $PID has terminated successfully."
            exit 0
        fi
    done

    echo "The process $PID is still running after 5 seconds!"

else
    echo "No running Python Console Application process found!"
fi
