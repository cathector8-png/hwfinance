#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=========================================="
echo " Installing hwfinance on Fedora Workstation"
echo "=========================================="

# 1. Install system dependencies if needed (Fedora uses dnf)
echo "--> Checking system dependencies..."
sudo dnf install -p python3-pip python3-tkinter -y

# 2. Install Python requirements
echo "--> Installing Python dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found, skipping pip install."
fi

# 3. Make the script executable
echo "--> Setting execution permissions..."
chmod +x TheBrains.py

# 4. Create a symlink in /usr/local/bin (Safe from DNF system overrides)
echo "--> Creating global system shortcut..."
sudo ln -sf "$(pwd)/TheBrains.py" /usr/local/bin/hwfinance

echo "=========================================="
echo " Success! Type 'hwfinance' to run the engine."
echo "=========================================="
