#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

# Simple validation script for Teo der Topf build system

set -e

echo "=== Teo der Topf Build System Validation ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_passed() {
    echo -e "${GREEN}✓${NC} $1"
}

test_failed() {
    echo -e "${RED}✗${NC} $1"
    return 1
}

test_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Get script directory and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

echo "Working directory: $PROJECT_DIR"
echo ""

# Test 1: Check if all required files exist
echo "1. Checking required files..."

required_files=(
    "main.py"
    "version.py"
    "requirements.txt"
    ".env"
    "app.sh"
    "stop_app.sh"
    "teo-der-topf.service"
    "scripts/firstrun.sh"
    "scripts/build_image.sh"
    "scripts/start_app.sh"
    ".github/workflows/build-raspberry-pi-image.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        test_passed "$file exists"
    else
        test_failed "$file is missing"
    fi
done

echo ""

# Test 2: Check Python syntax
echo "2. Checking Python syntax..."

if python3 -m py_compile main.py; then
    test_passed "main.py compiles"
else
    test_failed "main.py has syntax errors"
fi

if python3 -c "exec(open('version.py').read()); print('Version:', __version__)" > /dev/null; then
    VERSION=$(python3 -c "exec(open('version.py').read()); print(__version__)")
    test_passed "version.py is valid (version: $VERSION)"
else
    test_failed "version.py has errors"
fi

# Test Application directory
if [ -d "Application" ]; then
    test_passed "Application directory exists"
    
    # Test all Python files in Application
    python_files_ok=true
    for py_file in $(find Application -name "*.py"); do
        if python3 -m py_compile "$py_file"; then
            test_passed "$py_file compiles"
        else
            test_failed "$py_file has syntax errors"
            python_files_ok=false
        fi
    done
    
    if [ "$python_files_ok" = true ]; then
        test_passed "All Python files compile successfully"
    fi
else
    test_failed "Application directory is missing"
fi

echo ""

# Test 3: Check shell script syntax
echo "3. Checking shell script syntax..."

shell_scripts=(
    "app.sh"
    "stop_app.sh"
    "scripts/firstrun.sh"
    "scripts/build_image.sh"
    "scripts/start_app.sh"
)

for script in "${shell_scripts[@]}"; do
    if [ -f "$script" ]; then
        if bash -n "$script"; then
            test_passed "$script syntax is valid"
        else
            test_failed "$script has syntax errors"
        fi
        
        if [ -x "$script" ]; then
            test_passed "$script is executable"
        else
            test_warning "$script is not executable (fixing...)"
            chmod +x "$script"
            test_passed "$script made executable"
        fi
    fi
done

echo ""

# Test 4: Check systemd service file
echo "4. Checking systemd service file..."

if [ -f "teo-der-topf.service" ]; then
    test_passed "systemd service file exists"
    
    # Basic syntax check
    if grep -q "\[Unit\]" teo-der-topf.service && \
       grep -q "\[Service\]" teo-der-topf.service && \
       grep -q "\[Install\]" teo-der-topf.service; then
        test_passed "systemd service file has correct structure"
    else
        test_failed "systemd service file is malformed"
    fi
else
    test_failed "systemd service file is missing"
fi

echo ""

# Test 5: Check requirements.txt
echo "5. Checking requirements.txt..."

if [ -f "requirements.txt" ]; then
    test_passed "requirements.txt exists"
    
    # Check if requirements file is readable
    if [ -r "requirements.txt" ] && [ -s "requirements.txt" ]; then
        test_passed "requirements.txt is readable and not empty"
        echo "   Found $(wc -l < requirements.txt) package requirements"
    else
        test_warning "requirements.txt might be empty or unreadable"
    fi
else
    test_failed "requirements.txt is missing"
fi

echo ""

# Test 6: Check GitHub Actions workflow
echo "6. Checking GitHub Actions workflow..."

workflow_file=".github/workflows/build-raspberry-pi-image.yml"
if [ -f "$workflow_file" ]; then
    test_passed "GitHub Actions workflow exists"
    
    # Check basic YAML structure
    if grep -q "name:" "$workflow_file" && \
       grep -q "on:" "$workflow_file" && \
       grep -q "jobs:" "$workflow_file"; then
        test_passed "workflow file has correct YAML structure"
    else
        test_failed "workflow file is malformed"
    fi
    
    # Check for key workflow elements
    if grep -q "build-image:" "$workflow_file"; then
        test_passed "build-image job found"
    else
        test_warning "build-image job not found"
    fi
    
    if grep -q "runs-on: ubuntu-latest" "$workflow_file"; then
        test_passed "workflow uses ubuntu-latest runner"
    else
        test_warning "workflow runner not configured correctly"
    fi
else
    test_failed "GitHub Actions workflow is missing"
fi

echo ""

# Test 7: Directory structure
echo "7. Checking directory structure..."

expected_dirs=(
    "Application"
    "scripts"
    ".github/workflows"
)

for dir in "${expected_dirs[@]}"; do
    if [ -d "$dir" ]; then
        test_passed "$dir/ directory exists"
    else
        test_failed "$dir/ directory is missing"
    fi
done

echo ""

# Test 8: Check for potential issues
echo "8. Checking for potential issues..."

# Check for binary files in requirements.txt
if grep -i "^-e\|^git+\|^hg+\|^svn+\|^bzr+" requirements.txt >/dev/null 2>&1; then
    test_warning "requirements.txt contains VCS dependencies (may cause build issues)"
else
    test_passed "requirements.txt contains only PyPI packages"
fi

# Check .gitignore
if [ -f ".gitignore" ]; then
    test_passed ".gitignore exists"
    if grep -q "build/" .gitignore; then
        test_passed ".gitignore excludes build artifacts"
    else
        test_warning ".gitignore might not exclude build artifacts"
    fi
else
    test_warning ".gitignore is missing"
fi

echo ""

# Summary
echo "=== Validation Summary ==="
echo "✓ Build system files are present and syntactically correct"
echo "✓ Python application compiles without errors"
echo "✓ Shell scripts have valid syntax"
echo "✓ GitHub Actions workflow is properly structured"
echo ""
echo "Ready for image building!"
echo ""
echo "To build an image:"
echo "  Manual:  ./scripts/build_image.sh"
echo "  GitHub:  Use Actions tab in GitHub repository"
echo ""
echo "To test locally:"
echo "  ./app.sh  (manual start)"
echo "  sudo systemctl start teo-der-topf  (systemd service)"