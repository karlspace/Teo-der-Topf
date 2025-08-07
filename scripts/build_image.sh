#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Comprehensive Raspberry Pi image building script for Teo der Topf
# Supports both GitHub Actions and manual building

set -e

# Configuration
PI_OS_VERSION="${PI_OS_VERSION:-2024-03-15-raspios-bookworm-armhf-lite}"
BUILD_DIR="${BUILD_DIR:-build}"
IMAGE_NAME="${IMAGE_NAME:-teo-der-topf}"
DEBUG_MODE="${DEBUG_MODE:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get version information
get_version() {
    if [ -n "$CUSTOM_VERSION" ]; then
        echo "$CUSTOM_VERSION"
    else
        python3 -c "exec(open('version.py').read()); print(__version__)"
    fi
}

# Cleanup function
cleanup() {
    log "Cleaning up..."
    sudo umount "$BUILD_DIR/image/mnt/boot" 2>/dev/null || true
    sudo umount "$BUILD_DIR/image/mnt/root" 2>/dev/null || true
    sudo losetup -d /dev/loop0 2>/dev/null || true
    if [ "$DEBUG_MODE" != "true" ]; then
        rm -rf /tmp/workspace 2>/dev/null || true
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    local missing_tools=()
    
    for tool in wget xz unzip kpartx losetup; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log "Please install missing tools. On Ubuntu/Debian:"
        log "sudo apt-get install wget xz-utils unzip kpartx util-linux"
        exit 1
    fi
    
    if [ "$EUID" -eq 0 ]; then
        log_error "Don't run this script as root!"
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create build environment
setup_build_env() {
    log "Setting up build environment..."
    
    mkdir -p "$BUILD_DIR"/{image,scripts,config}
    
    VERSION=$(get_version)
    BUILD_DATE=$(date -u +'%Y-%m-%d_%H-%M-%S')
    GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    FINAL_IMAGE_NAME="${IMAGE_NAME}-${VERSION}"
    
    log "Version: $VERSION"
    log "Build date: $BUILD_DATE"
    log "Git hash: $GIT_HASH"
    log "Final image name: $FINAL_IMAGE_NAME"
    
    export VERSION BUILD_DATE GIT_HASH FINAL_IMAGE_NAME
}

# Download base image
download_base_image() {
    log "Downloading Raspberry Pi OS base image..."
    
    cd "$BUILD_DIR/image"
    
    if [ ! -f "raspios-lite.img" ]; then
        local image_url="https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2024-03-15/${PI_OS_VERSION}.img.xz"
        
        log "Downloading from: $image_url"
        wget -O raspios-lite.img.xz "$image_url"
        
        log "Extracting image..."
        xz -d raspios-lite.img.xz
        mv "${PI_OS_VERSION}.img" raspios-lite.img
        
        log_success "Base image downloaded and extracted"
    else
        log "Base image already exists, skipping download"
    fi
    
    cd - > /dev/null
}

# Create image customization script
create_setup_script() {
    log "Creating image setup script..."
    
    cat > "$BUILD_DIR/scripts/setup_image.sh" << 'EOF'
#!/bin/bash
set -e

MOUNT_BOOT="$1"
MOUNT_ROOT="$2"
DEBUG_MODE="$3"

echo "=== Setting up Teo der Topf Application ==="

# Copy application files
echo "Copying application files..."
cp -r /workspace/* "${MOUNT_ROOT}/home/iot/"
chown -R 1000:1000 "${MOUNT_ROOT}/home/iot/"

# Copy systemd service
echo "Installing systemd service..."
cp /workspace/teo-der-topf.service "${MOUNT_ROOT}/etc/systemd/system/"

# Install required packages
echo "Installing required packages..."
chroot "${MOUNT_ROOT}" apt-get update
chroot "${MOUNT_ROOT}" apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-pil \
    fonts-dejavu \
    i2c-tools \
    libopenjp2-7 \
    git \
    vim \
    mc \
    build-essential \
    cmake

# Create default user
echo "Setting up default user..."
if ! chroot "${MOUNT_ROOT}" id iot &>/dev/null; then
    chroot "${MOUNT_ROOT}" useradd -m -s /bin/bash iot
    echo "iot:iot2023!" | chroot "${MOUNT_ROOT}" chpasswd
    chroot "${MOUNT_ROOT}" usermod -aG sudo,spi,i2c,gpio,dialout iot
fi

# Enable services
echo "Enabling services..."
chroot "${MOUNT_ROOT}" systemctl enable ssh
chroot "${MOUNT_ROOT}" systemctl enable teo-der-topf.service

# Copy firstrun script for Pi Imager support
echo "Setting up Pi Imager support..."
cp /workspace/scripts/firstrun.sh "${MOUNT_BOOT}/firstrun.sh"
chmod +x "${MOUNT_BOOT}/firstrun.sh"

# Modify cmdline.txt for firstrun support
sed -i '1s/$/ systemd.run=\/boot\/firstrun.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target/' "${MOUNT_BOOT}/cmdline.txt"

# Configure hardware in config.txt
echo "Configuring hardware..."
cat >> "${MOUNT_BOOT}/config.txt" << 'CONFIG_EOF'

# Teo der Topf Hardware Configuration
dtparam=spi=on
dtparam=i2c_arm=on
dtparam=i2s=on
enable_uart=1
gpu_mem=128

# Audio
dtparam=audio=on
CONFIG_EOF

# Create build info
cat > "${MOUNT_ROOT}/home/iot/build_info.txt" << BUILD_INFO_EOF
Teo der Topf - Raspberry Pi Image
Build Date: $(date -u)
Version: ${VERSION}
Git Hash: ${GIT_HASH}
Base Image: ${PI_OS_VERSION}
Builder: GitHub Actions

Default Credentials (if not set via Pi Imager):
Username: iot
Password: iot2023!

Hardware Configuration:
- SPI: Enabled (ILI9341 Display)
- I2C: Enabled (BH1750, BMP280, ADS1115)
- UART: Enabled
- I2S: Enabled
- GPU Memory: 128MB

Services:
- SSH: Enabled
- Teo der Topf: Enabled (systemd)

Pi Imager Support:
- WiFi Configuration: ✓
- SSH Setup: ✓
- User Management: ✓
- Locale Settings: ✓

For more information, see README.MD
BUILD_INFO_EOF

chown 1000:1000 "${MOUNT_ROOT}/home/iot/build_info.txt"

echo "=== Image setup completed ==="
EOF

    chmod +x "$BUILD_DIR/scripts/setup_image.sh"
    log_success "Setup script created"
}

# Customize the image
customize_image() {
    log "Customizing Raspberry Pi image..."
    
    cd "$BUILD_DIR/image"
    
    # Show original size
    local original_size=$(stat -c%s raspios-lite.img)
    log "Original image size: $(( original_size / 1024 / 1024 )) MB"
    
    # Create loop device
    log "Creating loop device..."
    sudo losetup -P /dev/loop0 raspios-lite.img
    
    # Wait for partitions
    sleep 3
    
    # Create mount points
    mkdir -p mnt/{boot,root}
    
    # Mount partitions
    log "Mounting partitions..."
    sudo mount /dev/loop0p1 mnt/boot
    sudo mount /dev/loop0p2 mnt/root
    
    # Prepare workspace
    log "Preparing application workspace..."
    mkdir -p /tmp/workspace
    cp -r ../../* /tmp/workspace/
    rm -rf /tmp/workspace/.git /tmp/workspace/build
    
    # Run setup script
    log "Running image customization..."
    sudo ../scripts/setup_image.sh \
        "$(pwd)/mnt/boot" \
        "$(pwd)/mnt/root" \
        "$DEBUG_MODE"
    
    # Cleanup mounts
    log "Unmounting and cleaning up..."
    sudo umount mnt/boot mnt/root
    sudo losetup -d /dev/loop0
    
    # Rename to final name
    mv raspios-lite.img "${FINAL_IMAGE_NAME}.img"
    
    cd - > /dev/null
    log_success "Image customization completed"
}

# Optimize image size
optimize_image() {
    log "Optimizing image size..."
    
    cd "$BUILD_DIR/image"
    
    # Create loop device for optimization
    sudo losetup -P /dev/loop0 "${FINAL_IMAGE_NAME}.img"
    sleep 2
    
    # Zero unused blocks (if zerofree is available)
    if command -v zerofree &> /dev/null; then
        log "Running zerofree to optimize unused space..."
        sudo zerofree /dev/loop0p2 || log_warning "zerofree failed, continuing..."
    else
        log_warning "zerofree not available, skipping space optimization"
    fi
    
    sudo losetup -d /dev/loop0
    
    local optimized_size=$(stat -c%s "${FINAL_IMAGE_NAME}.img")
    log "Optimized image size: $(( optimized_size / 1024 / 1024 )) MB"
    
    cd - > /dev/null
    log_success "Image optimization completed"
}

# Create final artifacts
create_artifacts() {
    log "Creating final artifacts..."
    
    cd "$BUILD_DIR/image"
    
    # Compress image
    log "Compressing image..."
    zip -9 "${FINAL_IMAGE_NAME}.zip" "${FINAL_IMAGE_NAME}.img"
    
    # Generate checksums
    log "Generating checksums..."
    sha256sum "${FINAL_IMAGE_NAME}.img" > "${FINAL_IMAGE_NAME}.img.sha256"
    sha256sum "${FINAL_IMAGE_NAME}.zip" > "${FINAL_IMAGE_NAME}.zip.sha256"
    md5sum "${FINAL_IMAGE_NAME}.img" > "${FINAL_IMAGE_NAME}.img.md5"
    md5sum "${FINAL_IMAGE_NAME}.zip" > "${FINAL_IMAGE_NAME}.zip.md5"
    
    # Create manifest
    log "Creating build manifest..."
    cat > manifest.txt << EOF
Teo der Topf - Raspberry Pi Image Build Manifest
===============================================

Build Information:
- Version: $VERSION
- Build Date: $BUILD_DATE
- Git Hash: $GIT_HASH
- Base Image: $PI_OS_VERSION
- Builder: $(whoami)@$(hostname)

Files:
- Image: ${FINAL_IMAGE_NAME}.img
- Compressed: ${FINAL_IMAGE_NAME}.zip
- Checksums: .sha256 and .md5 files

Raspberry Pi Imager Support: ✓ Full Support
- WiFi Configuration: Supported
- SSH Activation: Supported
- User Setup: Supported
- Advanced Options: Fully Compatible

Default Configuration (if not set via Pi Imager):
- Username: iot
- Password: iot2023!
- SSH: Enabled
- Hardware: SPI, I2C, UART, I2S enabled

Installation Instructions:
1. Download and install Raspberry Pi Imager
2. Flash the .img file to a microSD card (8GB minimum)
3. Use advanced options in Pi Imager to configure WiFi, SSH, and user
4. Insert SD card into Raspberry Pi and boot
5. Application starts automatically via systemd service

For manual setup or troubleshooting, see README.MD
EOF
    
    # Show final results
    log_success "=== Build Results ==="
    ls -lh "${FINAL_IMAGE_NAME}".*
    
    cd - > /dev/null
}

# Main execution
main() {
    log "Starting Teo der Topf Raspberry Pi image build..."
    
    check_prerequisites
    setup_build_env
    download_base_image
    create_setup_script
    customize_image
    optimize_image
    create_artifacts
    
    log_success "Build completed successfully!"
    log "Image location: $BUILD_DIR/image/${FINAL_IMAGE_NAME}.zip"
    log "Manifest: $BUILD_DIR/image/manifest.txt"
}

# Run main function
main "$@"