#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Pi Imager firstrun.sh script for advanced options support
# This script runs on first boot and handles Pi Imager configurations

set +e

echo "=== Teo der Topf - Pi Imager First Run Setup ==="

CURRENT_HOSTNAME=$(cat /etc/hostname | tr -d " \t\n\r")

# Enable SSH if configured via Pi Imager
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
  /usr/lib/raspberrypi-sys-mods/imager_custom enable_ssh
fi

# Handle user configuration from Pi Imager
USER_CONFIGURED=false

# Check for userconf.txt (Pi Imager user setup) in both possible locations
for USERCONF_PATH in /boot/userconf.txt /boot/firmware/userconf.txt; do
  if [ -f "$USERCONF_PATH" ]; then
    echo "Pi Imager user configuration found at $USERCONF_PATH"
    USER_CONFIGURED=true
    
    # Extract username from userconf.txt (format: username:encrypted_password)
    IMAGER_USER=$(cut -d':' -f1 "$USERCONF_PATH")
    echo "Pi Imager configured user: $IMAGER_USER"
    
    # Add user to required groups for hardware access
    usermod -aG sudo,spi,i2c,gpio,dialout "$IMAGER_USER"
    
    # Copy application files to Pi Imager user home if not 'iot'
    if [ "$IMAGER_USER" != "iot" ] && [ -d "/home/iot" ]; then
      echo "Copying application files to Pi Imager user home..."
      cp -r /home/iot/* "/home/$IMAGER_USER/"
      chown -R "$IMAGER_USER:$IMAGER_USER" "/home/$IMAGER_USER/"
      
      # Update systemd service to use Pi Imager user
      sed -i "s/User=iot/User=$IMAGER_USER/g" /etc/systemd/system/teo-der-topf.service
      sed -i "s/Group=iot/Group=$IMAGER_USER/g" /etc/systemd/system/teo-der-topf.service
      sed -i "s|WorkingDirectory=/home/iot|WorkingDirectory=/home/$IMAGER_USER|g" /etc/systemd/system/teo-der-topf.service
      sed -i "s|/home/iot|/home/$IMAGER_USER|g" /etc/systemd/system/teo-der-topf.service
    fi
    
    # Remove userconf.txt for security
    rm -f "$USERCONF_PATH"
    break
  fi
done

# Fallback to default user if no Pi Imager user configured
if [ "$USER_CONFIGURED" = false ]; then
  echo "No Pi Imager user configuration found, using default user 'iot'"
  
  # Create default user if it doesn't exist
  if ! id iot &>/dev/null; then
    useradd -m -s /bin/bash iot
    echo "iot:iot2023!" | chpasswd
    usermod -aG sudo,spi,i2c,gpio,dialout iot
    echo "Created default user 'iot' with password 'iot2023!'"
  fi
fi

# Enable SSH by default (will be overridden by Pi Imager if configured)
systemctl enable ssh

# Enable hardware interfaces
echo "Enabling hardware interfaces..."

# SPI for display
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
  echo "dtparam=spi=on" >> /boot/config.txt
fi

# I2C for sensors
if ! grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
  echo "dtparam=i2c_arm=on" >> /boot/config.txt
fi

# UART
if ! grep -q "enable_uart=1" /boot/config.txt; then
  echo "enable_uart=1" >> /boot/config.txt
fi

# I2S
if ! grep -q "dtparam=i2s=on" /boot/config.txt; then
  echo "dtparam=i2s=on" >> /boot/config.txt
fi

# GPU memory
if ! grep -q "gpu_mem" /boot/config.txt; then
  echo "gpu_mem=128" >> /boot/config.txt
fi

# Enable and start Teo der Topf service
systemctl daemon-reload
systemctl enable teo-der-topf.service

echo "=== First run setup completed ==="

# Clean up firstrun.sh and cmdline.txt
rm -f /boot/firstrun.sh /boot/firmware/firstrun.sh
sed -i 's| systemd.run.*||g' /boot/cmdline.txt

# Create completion marker
echo "$(date): First run setup completed successfully" > /home/*/teo_firstrun_complete.txt

exit 0