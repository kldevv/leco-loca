#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_folder destination_folder"
    exit 1
fi

# Assign source and destination folder variables
src_folder="$1"
dst_folder="$2"

# Check if the source folder exists
if [ ! -d "$src_folder" ]; then
    echo "Error: Source folder '$src_folder' does not exist."
    exit 1
fi

# Create the destination folder if it doesn't exist
if [ ! -d "$dst_folder" ]; then
    mkdir -p "$dst_folder"
fi

# Copy all contents from the source folder to the destination folder
cp -r "$src_folder"/* "$dst_folder"

echo "All contents from '$src_folder' have been copied to '$dst_folder'."
