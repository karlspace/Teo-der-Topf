#!/bin/bash

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

REPO_URL="https://github.com/bauer-group/BAUERGROUPKidsToysTeoTopf.git"
CLONE_PATH="$HOME/teotopf"

function update_packages() {
    echo "Updating package lists..."
    sudo apt-get update
}

function install_git() {
    if ! command -v git &> /dev/null
    then
        echo "Git is not installed. Installing..."
        sudo apt-get install -y git
    else
        echo "Git is already installed."
    fi
}

function clone_repository() {
    if [ ! -d "$CLONE_PATH" ]; then
        echo "Specified path doesn't exist. Creating..."
        mkdir -p "$CLONE_PATH"
    fi

    cd "$CLONE_PATH"

    echo "Cloning the latest snapshot of the repository..."
    git clone --depth 1 "$REPO_URL" .
}

function run_setup() {
    echo "Running the ApplicationSetup.sh..."
    if [ -f "ApplicationSetup.sh" ]; then
        chmod +x ApplicationSetup.sh
        ./ApplicationSetup.sh
    else
        echo "ApplicationSetup.sh does not exist in the cloned repository. Please check the repository content."
    fi
}

function main() {
    echo "One-CLick-Setup starting..."

    update_packages
    install_git
    clone_repository
    run_setup

    echo "One-Click-Setup finished..."
}

# Start script execution
main


#USE: curl -sSL https://raw.githubusercontent.com/username/repo/master/setup.sh | bash
#USE: wget -O - https://raw.githubusercontent.com/username/repo/master/setup.sh | bash
