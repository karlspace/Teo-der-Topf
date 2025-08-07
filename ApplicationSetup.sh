#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

OSSetup() {
    # Use raspi-config in non-interactive mode

    # Enable UART
    sudo raspi-config nonint do_serial 0

    # Enable SPI
    sudo raspi-config nonint do_spi 0

    # Enable I2S
    sudo raspi-config nonint do_i2s 0

    # Enable I2C
    sudo raspi-config nonint do_i2c 0

    # Reboot
    echo "REBOOT IS REQUIRED, do you want to reboot now? (y/n)"
    read answer
    if [ "$answer" == "y" ]; then
        sudo reboot
    fi
}

SetupAutologin() {
    local AUTOLOGIN_SERVICE="/etc/systemd/system/getty@tty1.service.d/autologin.conf"
    local USERNAME=$(whoami)

    # Create the service directory if it does not exist
    if [ ! -d "$(dirname $AUTOLOGIN_SERVICE)" ]; then
        sudo mkdir -p "$(dirname $AUTOLOGIN_SERVICE)"
    fi

    # Create the autologin service
    echo "[Service]" | sudo tee $AUTOLOGIN_SERVICE
    echo "ExecStart=" | sudo tee -a $AUTOLOGIN_SERVICE
    echo "ExecStart=-/sbin/agetty --autologin $USERNAME --noclear %I \$TERM" | sudo tee -a $AUTOLOGIN_SERVICE
}

InstallPackages() {
    sudo apt-get update -y
    sudo apt-get install -y vim mc git make gcc cmake build-essential python3 python3-pip python3-venv python3-pil fonts-dejavu i2c-tools libopenjp2-7
}

SetupAppEntry() {
    local SCRIPT_DIR=$(dirname "$0")
    local APP_PATH_RUN="$SCRIPT_DIR/app.sh"
    local APP_PATH_STOP="$SCRIPT_DIR/stop_app.sh"

    # Make sure app.sh is executable
    if [ ! -x "$APP_PATH_RUN" ]; then
        chmod +x "$APP_PATH_RUN"
    fi

    # Make sure stop_app.sh is executable
    if [ ! -x "APP_PATH_STOP" ]; then
        chmod +x "APP_PATH_STOP"
    fi

    # Check the preferred profile file and add the execution command
    local PROFILE_FILES=("$HOME/.bash_profile" "$HOME/.bash_login" "$HOME/.profile")
    for PROFILE_FILE in "${PROFILE_FILES[@]}"; do
        if [ -f "$PROFILE_FILE" ]; then
            echo "Adding application entry point to $PROFILE_FILE"
            echo "" >> "$PROFILE_FILE"
			echo "sleep 10;" >> "$PROFILE_FILE"
            echo "$APP_PATH_RUN" >> "$PROFILE_FILE"
            break
        fi
    done
}

echo "=== Configure the Environment for the Application === "

echo "Installing Packages"
InstallPackages

echo "Enable Autologin for User $(whoami)"
SetupAutologin

echo "Create Autostart for Application Entrypoint"
SetupAppEntry

echo "Configure Hardware / Kernel"
OSSetup

echo ">>> Setup is Complete... <<<"
