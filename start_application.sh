#!/bin/bash

# This script shows how to run the Old TV Mirror application

echo "Starting Old TV Mirror Application"
echo "=================================="

# Check if camera is available
if ! v4l2-ctl --list-devices > /dev/null 2>&1; then
    echo "Warning: v4l2-ctl not found. Camera detection may be limited."
fi

# Try to run the main application
echo "Running main application..."
python3 main.py