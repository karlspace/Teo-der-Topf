# Teo der Topf - Raspberry Pi Image Building

This directory contains scripts and configurations for building a complete Raspberry Pi image for Teo der Topf with full Pi Imager support.

## 🚀 Quick Start (GitHub Actions)

The easiest way to build an image is using GitHub Actions:

1. Go to the [Actions tab](../../actions) in GitHub
2. Select "Build Raspberry Pi Image for Teo der Topf"
3. Click "Run workflow"
4. Wait for the build to complete (~30-45 minutes)
5. Download the artifacts from the completed workflow

## 🛠️ Manual Building

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    qemu-user-static \
    binfmt-support \
    wget \
    xz-utils \
    zip \
    unzip \
    kpartx \
    util-linux \
    zerofree
```

**Other distributions:** Install equivalent packages for your system.

### Build Process

1. **Clone the repository:**
   ```bash
   git clone https://github.com/karlspace/Teo-der-Topf.git
   cd Teo-der-Topf
   ```

2. **Run the build script:**
   ```bash
   chmod +x scripts/build_image.sh
   ./scripts/build_image.sh
   ```

3. **Find your image:**
   ```bash
   ls -la build/image/teo-der-topf-*.zip
   ```

### Build Configuration

You can customize the build by setting environment variables:

```bash
# Custom version
CUSTOM_VERSION="1.0.0-beta" ./scripts/build_image.sh

# Debug mode (keeps temporary files)
DEBUG_MODE="true" ./scripts/build_image.sh

# Custom base image version
PI_OS_VERSION="2024-03-15-raspios-bookworm-armhf-lite" ./scripts/build_image.sh
```

## 📁 File Structure

```
scripts/
├── build_image.sh          # Main build script (manual building)
├── firstrun.sh            # Pi Imager first-run script
└── start_app.sh           # Enhanced startup script

teo-der-topf.service       # Systemd service file
.github/workflows/
└── build-raspberry-pi-image.yml  # GitHub Actions workflow
```

## 🔧 Pi Imager Integration

The built image includes full support for Raspberry Pi Imager's advanced options:

### Supported Features

- ✅ **WiFi Configuration**: Set SSID and password via UI
- ✅ **SSH Setup**: Enable SSH and set authentication
- ✅ **User Management**: Create custom user instead of default 'iot'
- ✅ **Locale Settings**: Configure keyboard, timezone, etc.
- ✅ **Hostname**: Set custom device name

### How It Works

1. **firstrun.sh**: Runs on first boot, handles Pi Imager configurations
2. **Fallback Support**: Uses default user 'iot' if no Pi Imager config
3. **Service Adaptation**: Automatically adjusts systemd service for custom users
4. **Hardware Setup**: Enables SPI, I2C, UART, I2S regardless of configuration

## 🎯 Build Outputs

Each build produces:

- **`teo-der-topf-{version}.img`**: Raw disk image
- **`teo-der-topf-{version}.zip`**: Compressed image (recommended)
- **`.sha256` and `.md5`**: Checksums for verification
- **`manifest.txt`**: Build information and instructions

## 🔒 Security Features

- **No hardcoded credentials** in the image (except fallback)
- **Service isolation** with systemd security options
- **Secure defaults** with Pi Imager user management
- **Automatic cleanup** of sensitive files after first run

## 🐛 Troubleshooting

### Build Issues

**"Permission denied" errors:**
- Don't run as root
- Check that your user can use sudo
- Ensure loop devices are available

**"Command not found" errors:**
- Install missing prerequisites
- Check your PATH environment

**Download failures:**
- Check internet connectivity
- Verify Raspberry Pi OS download URLs are current

### Runtime Issues

**Application not starting:**
```bash
# Check service status
sudo systemctl status teo-der-topf

# View logs
sudo journalctl -u teo-der-topf -f

# Manual start for debugging
cd /home/iot
./scripts/start_app.sh
```

**Hardware not detected:**
```bash
# Check I2C devices
i2cdetect -y 1

# Check SPI
ls -la /dev/spidev*

# Check hardware config
cat /boot/config.txt | grep -E "(spi|i2c|uart|i2s)"
```

### Getting Help

1. Check the logs: `sudo journalctl -u teo-der-topf -f`
2. Verify hardware connections match the [README.MD](../README.MD)
3. Test sensors individually with the provided scripts
4. Create an issue with logs and system information

## 🔄 Development Workflow

### Testing Changes

1. Make your changes to the application
2. Update `version.py` if needed
3. Test locally: `python3 main.py`
4. Run build script: `./scripts/build_image.sh`
5. Test image on actual hardware

### Automated Builds

- **Pushes to main**: No automatic builds
- **Tags (v*)**: Automatic build and release
- **Manual trigger**: Via GitHub Actions UI
- **Releases**: Automatic artifact upload

### Customizing the Build

**Adding packages:**
Edit the `apt-get install` section in the build script.

**Changing default user:**
Modify the `firstrun.sh` script and systemd service.

**Hardware configuration:**
Update the `config.txt` modifications in the build script.

## 📊 Build Performance

Typical build times:
- **GitHub Actions**: 30-45 minutes
- **Local (SSD)**: 15-25 minutes  
- **Local (HDD)**: 25-40 minutes

Image sizes:
- **Uncompressed**: ~4-6 GB
- **Compressed**: ~1.5-2.5 GB
- **Minimum SD Card**: 8 GB

## 🌟 Features Included

- **Complete Application**: Teo der Topf with all dependencies
- **Virtual Environment**: Isolated Python packages
- **Systemd Service**: Reliable startup and crash recovery
- **Hardware Support**: All sensors and display pre-configured
- **Pi Imager Ready**: Full advanced options support
- **SSH Access**: Enabled by default with secure setup
- **Development Tools**: vim, mc, git for on-device development

## 📝 License

Scripts and configurations are licensed under MIT License.
See [LICENSE](../LICENSE) for details.