---
name: Hardware/Runtime Issue
about: Report problems with the application running on Raspberry Pi
title: '[RUNTIME] '
labels: ['runtime', 'hardware']
assignees: ''

---

## Hardware Setup
- **Raspberry Pi Model**: (e.g., Pi Zero W, Pi 4 Model B)
- **Image Used**: (e.g., teo-der-topf-0.3.0.zip from releases, manual installation)
- **SD Card**: (size and brand if known)
- **Display**: (e.g., ILI9341 320x240)
- **Sensors Connected**: 
  - [ ] BH1750 Light Sensor
  - [ ] BMP280 Temperature/Pressure
  - [ ] ADS1115 + Soil Sensor
  - [ ] Other:

## Issue Description
<!-- Describe what's not working -->

## Expected Behavior
<!-- What should happen? -->

## Actual Behavior
<!-- What actually happens? -->

## System Information
<!-- Run these commands on your Pi and paste the output -->

**Service Status:**
```bash
sudo systemctl status teo-der-topf
```

**Hardware Detection:**
```bash
# I2C devices
i2cdetect -y 1

# SPI devices
ls -la /dev/spidev*

# Hardware config
cat /boot/config.txt | grep -E "(spi|i2c|uart|i2s)"
```

**Application Logs:**
```bash
sudo journalctl -u teo-der-topf -n 50 --no-pager
```

**System Info:**
```bash
# Pi model and OS
cat /proc/device-tree/model && echo
cat /etc/os-release | grep PRETTY_NAME

# Memory and disk
free -h
df -h /
```

## Troubleshooting Attempted
<!-- What have you already tried? -->
- [ ] Restarted the Pi
- [ ] Checked connections
- [ ] Reviewed logs
- [ ] Tested sensors individually
- [ ] Other:

## Additional Context
<!-- Any other relevant information -->

## Configuration
<!-- If you modified any configuration files -->
- [ ] Modified .env file
- [ ] Changed hardware connections
- [ ] Custom sensor calibration
- [ ] Other modifications: