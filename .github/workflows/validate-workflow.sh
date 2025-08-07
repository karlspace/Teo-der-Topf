#!/bin/bash

# Teo der Topf - Workflow Validation Script
# This script validates the GitHub Actions workflow without actually running it

set -e

echo "🔍 Teo der Topf - Workflow Validation"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "version.py" ] || [ ! -f "main.py" ]; then
    echo "❌ Error: Not in the Teo der Topf project root"
    exit 1
fi

echo "✅ Project structure validated"

# Check if workflow file exists and is valid YAML
WORKFLOW_FILE=".github/workflows/build-teo-image.yml"
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Error: Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

echo "✅ Workflow file exists"

# Validate YAML syntax
if python3 -c "import yaml; yaml.safe_load(open('$WORKFLOW_FILE'))" 2>/dev/null; then
    echo "✅ Workflow YAML syntax is valid"
else
    echo "❌ Error: Invalid YAML syntax in workflow file"
    exit 1
fi

# Check version extraction
VERSION=$(python3 -c "exec(open('version.py').read()); print(__version__)" 2>/dev/null)
if [ -n "$VERSION" ]; then
    echo "✅ Version extraction works: $VERSION"
else
    echo "❌ Error: Cannot extract version from version.py"
    exit 1
fi

# Check required features in workflow
REQUIRED_FEATURES=(
    "firstrun.sh"
    "userconf.txt"
    "wpa_supplicant.conf"
    "iot2023!"
    "systemd"
    "python3 -m venv"
    "raspi-config nonint do_spi"
    "raspi-config nonint do_i2c"
    "requirements.txt"
    "sha256sum"
)

echo ""
echo "🔍 Checking required features:"

for feature in "${REQUIRED_FEATURES[@]}"; do
    if grep -q "$feature" "$WORKFLOW_FILE"; then
        echo "  ✅ $feature"
    else
        echo "  ❌ Missing: $feature"
        exit 1
    fi
done

# Check matrix configuration
if grep -q "pi_model:" "$WORKFLOW_FILE" && grep -q "zero-w" "$WORKFLOW_FILE" && grep -q "4b" "$WORKFLOW_FILE"; then
    echo "✅ Matrix build configuration found"
else
    echo "❌ Error: Matrix build configuration missing"
    exit 1
fi

# Check if all required steps are present
REQUIRED_STEPS=(
    "Checkout repository"
    "Get version from version.py"
    "Download Raspberry Pi OS base image"
    "Create Pi Imager compatibility files"
    "Install Teo der Topf application"
    "Configure Pi Imager support files"
    "Compress and create checksums"
    "Upload build artifacts"
)

echo ""
echo "🔍 Checking workflow steps:"

for step in "${REQUIRED_STEPS[@]}"; do
    if grep -q "$step" "$WORKFLOW_FILE"; then
        echo "  ✅ $step"
    else
        echo "  ❌ Missing step: $step"
        exit 1
    fi
done

# Check that the workflow has proper job dependencies
if grep -q "needs: prepare" "$WORKFLOW_FILE" && grep -q "needs: \[prepare, build-image\]" "$WORKFLOW_FILE"; then
    echo "✅ Job dependencies configured correctly"
else
    echo "❌ Error: Job dependencies not configured correctly"
    exit 1
fi

# Check file structure
if [ ! -d ".github/workflows" ]; then
    echo "❌ Error: .github/workflows directory missing"
    exit 1
fi

echo "✅ Directory structure correct"

# Summary
echo ""
echo "🎉 Workflow Validation Summary"
echo "=============================="
echo "✅ All required features present"
echo "✅ YAML syntax valid"
echo "✅ Version extraction working"
echo "✅ Matrix builds configured"
echo "✅ Pi Imager compatibility included"
echo "✅ Hardware optimization included"
echo "✅ Application setup included"
echo "✅ Professional packaging included"
echo ""
echo "🚀 The workflow is ready to build Raspberry Pi images!"
echo ""
echo "📝 To trigger a build:"
echo "   - Push changes to main/develop branch"
echo "   - Create a tag: git tag v$VERSION && git push origin v$VERSION"
echo "   - Manual trigger via GitHub Actions UI"
echo ""
echo "💡 Default credentials (fallback): iot / iot2023!"
echo "⚠️  Always configure via Pi Imager for security!"