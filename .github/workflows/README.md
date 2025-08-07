# Teo der Topf - Raspberry Pi Image Build Workflow

This directory contains the GitHub Actions workflow for automatically building ready-to-use Raspberry Pi images for the "Teo der Topf" project with full Raspberry Pi Imager compatibility.

## 🚀 Workflow Overview

The `build-teo-image.yml` workflow creates production-ready Raspberry Pi images that work seamlessly with the Raspberry Pi Imager's advanced configuration options.

### Key Features

- **🔧 Raspberry Pi Imager Compatible**: Full support for WiFi, SSH, user configuration
- **🎯 Multi-Model Support**: Optimized builds for Pi Zero W (32-bit) and Pi 4B (64-bit)
- **📦 Complete Application Setup**: Pre-installed with all dependencies and auto-start
- **🛡️ Robust Configuration**: Systemd service + fallback autostart mechanisms
- **📊 Professional Packaging**: Checksums, manifests, and detailed release notes

## 🔄 Workflow Triggers

The workflow runs automatically on:

- **Push to main/develop**: Builds images when relevant files change
- **Tag pushes (v*)**: Creates full releases with GitHub Releases
- **Pull requests**: Validates builds for main branch PRs
- **Manual trigger**: Force build via GitHub Actions UI

### Smart Build Detection

The workflow only builds when relevant files change:
- Python files (*.py)
- Shell scripts (*.sh) 
- Configuration files (*.txt, *.yml, *.yaml)
- Application directory changes
- Version or requirements updates

## 🏗️ Build Process

### 1. Preparation Stage
- Extracts version from `version.py`
- Checks for relevant file changes
- Sets up build metadata

### 2. Image Building (Matrix)
- Downloads official Raspberry Pi OS Lite (Bookworm)
- Creates separate builds for different Pi models:
  - **zero-w**: 32-bit ARM (Pi Zero W, Pi 3, etc.)
  - **4b**: 64-bit ARM (Pi 4B, Pi 5, etc.)

### 3. Customization
- Installs Teo der Topf application
- Configures hardware interfaces (SPI, I2C, UART, I2S)
- Sets up Python virtual environment
- Creates systemd service
- Adds Pi Imager compatibility scripts

### 4. Packaging
- Optimizes and cleans image
- Creates compressed ZIP archives
- Generates SHA256 checksums
- Creates detailed manifests

### 5. Release (for tags)
- Creates GitHub Release
- Uploads all artifacts
- Generates professional release notes

## 🎮 Raspberry Pi Imager Compatibility

### Supported Features

The built images fully support Raspberry Pi Imager's advanced options:

- ✅ **WiFi Configuration**: Automatically configured on first boot
- ✅ **SSH Access**: Enable SSH with your own keys
- ✅ **User Account**: Set custom username and password
- ✅ **Locale Settings**: Timezone, keyboard layout, WiFi country

### Graceful Fallbacks

If not configured via Pi Imager, the image provides sensible defaults:

- **Default Username**: `iot`
- **Default Password**: `iot2023!`
- **SSH**: Disabled (enable via Pi Imager or manually)
- **Application**: Still auto-starts on console login

### How It Works

The images include a `firstrun.sh` script that:

1. **Detects Pi Imager configuration** (userconf.txt, wpa_supplicant.conf, ssh file)
2. **Applies settings** or falls back to defaults
3. **Enables hardware interfaces** required by Teo der Topf
4. **Sets up the application** with virtual environment
5. **Configures auto-start** via systemd service + console fallback
6. **Removes itself** after successful setup

## 📁 Output Artifacts

For each Pi model, the workflow creates:

- `teo-der-topf-{model}-v{version}.zip` - Compressed disk image
- `teo-der-topf-{model}-v{version}.zip.sha256` - ZIP checksum
- `teo-der-topf-{model}-v{version}.img.sha256` - Image checksum  
- `teo-der-topf-{model}-v{version}.manifest.json` - Build metadata

### Manifest Contents

```json
{
  "name": "Teo der Topf Raspberry Pi Image",
  "version": "0.3.0",
  "model": "zero-w",
  "architecture": "armhf",
  "build_date": "2024-08-07T19:30:00Z",
  "base_os": "Raspberry Pi OS Lite (Bookworm)",
  "features": [
    "Raspberry Pi Imager Compatible",
    "Hardware Optimization (SPI, I2C, UART, I2S)",
    "Python Virtual Environment", 
    "Systemd Service",
    "Default User: iot/iot2023! (fallback)",
    "Auto WiFi/SSH/User Configuration Support"
  ],
  "default_credentials": {
    "username": "iot",
    "password": "iot2023!",
    "note": "Only used if not configured via Pi Imager"
  },
  "image_size_mb": 2048,
  "compressed_size_mb": 512
}
```

## 🔧 Usage Instructions

### For End Users

1. **Download** the appropriate image for your Pi model from GitHub Releases
2. **Flash** using Raspberry Pi Imager
3. **Configure** WiFi, SSH, and user account in Pi Imager (recommended)
4. **Boot** your Raspberry Pi - Teo der Topf starts automatically!

### For Developers

1. **Push changes** to trigger automatic builds
2. **Create tags** (v*) for full releases
3. **Monitor** build progress in GitHub Actions
4. **Download** artifacts for testing

## 🐛 Troubleshooting

### Build Failures

- Check GitHub Actions logs for specific error messages
- Verify YAML syntax if workflow files were modified
- Ensure adequate disk space (build uses ~8GB)

### Image Issues

- Verify SHA256 checksums after download
- Test images in emulator before flashing to hardware
- Check firstrun.sh script for configuration issues

### Pi Imager Problems

- Ensure you're using the latest Raspberry Pi Imager
- Advanced options require Imager v1.6+
- Some older versions may not support all features

## 📈 Performance

### Build Times
- **Preparation**: ~2 minutes
- **Image Download**: ~5 minutes
- **Customization**: ~10 minutes  
- **Compression**: ~5 minutes
- **Total per model**: ~22 minutes

### Disk Usage
- **Base image**: ~2GB
- **Customized image**: ~3GB
- **Compressed**: ~800MB
- **Working space**: ~8GB during build

## 🔐 Security

### Default Credentials
- Default password is publicly known - **change via Pi Imager**
- SSH disabled by default for security
- All software from official repositories

### Best Practices
- Always configure your own user via Pi Imager
- Enable SSH only if needed
- Change default passwords immediately
- Keep Pi Imager and images updated

## 🧪 Testing

### Automated Tests
- YAML syntax validation
- Version extraction verification
- File change detection logic

### Manual Validation
- Flash images to real hardware
- Test Pi Imager configuration scenarios
- Verify application auto-start
- Confirm sensor functionality

## 📚 Further Reading

- [Raspberry Pi Imager Documentation](https://www.raspberrypi.org/documentation/computers/getting-started.html#raspberry-pi-imager)
- [Pi OS Customization Guide](https://www.raspberrypi.org/documentation/computers/configuration.html)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Teo der Topf Project Documentation](../README.md)