#!/bin/bash

# This script will switch to the specified directory, run pytest, and clean temporary folders

# Set the target directory for testing
TARGET_DIR=$1

# Switch to the target directory
echo "Switching to the target directory: $TARGET_DIR"
cd "$TARGET_DIR"

# Check if the directory switch was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to switch to the target directory."
    exit 1
fi

# Run pytest
echo "Running pytest..."
if [[ "$2" == "-u" ]]; then
    pytest -v -rx -m unordered
elif [[ "$2" == "-c" ]]; then
    pytest -v -rx -m class_design
else
    pytest -v -rx -m ordered
fi

PYTEST_STATUS=$?

# Check if pytest ran successfully
if [ $PYTEST_STATUS -ne 0 ]; then
    echo "Error: pytest failed."
fi

# Clean temporary folders (__pycache__ and .pytest_cache)
echo "Cleaning temporary folders..."
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name ".pytest_cache" -exec rm -r {} +

# Check if the cleaning process was successful
if [ $? -eq 0 ]; then
    echo "Temporary folders cleaned successfully."
else
    echo "Error: Failed to clean temporary folders."
    exit 3
fi

# If pytest failed, exit with the pytest return status
if [ $PYTEST_STATUS -ne 0 ]; then
    exit 2
fi

echo "$0 $TARGET_DIR: completed successfully."
exit 0
