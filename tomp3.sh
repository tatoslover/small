#!/bin/bash

# Audio to MP3 Converter Script
# Converts m4a and wav files to mp3 using ffmpeg

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install ffmpeg first."
    exit 1
fi

# Function to convert a single file
convert_file() {
    local input_file="$1"
    local output_file="${input_file%.*}.mp3"

    echo "Converting: $input_file -> $output_file"

    # Convert with good quality settings
    ffmpeg -i "$input_file" -codec:a libmp3lame -b:a 192k "$output_file" -y

    if [ $? -eq 0 ]; then
        echo "✓ Successfully converted: $output_file"
    else
        echo "✗ Failed to convert: $input_file"
    fi
}

# Function to convert all supported files in current directory
convert_all() {
    local count=0

    # Convert m4a files
    for file in *.m4a; do
        if [ -f "$file" ]; then
            convert_file "$file"
            ((count++))
        fi
    done

    # Convert wav files
    for file in *.wav; do
        if [ -f "$file" ]; then
            convert_file "$file"
            ((count++))
        fi
    done

    if [ $count -eq 0 ]; then
        echo "No m4a or wav files found in current directory."
    else
        echo "Conversion complete! Processed $count files."
    fi
}

# Main script logic
if [ $# -eq 0 ]; then
    echo "Audio to MP3 Converter"
    echo "Usage:"
    echo "  $0 <file1> <file2> ...    # Convert specific files"
    echo "  $0 --all                  # Convert all m4a and wav files in current directory"
    echo ""
    echo "Supported formats: m4a, wav"
    exit 1
fi

# Handle --all flag
if [ "$1" == "--all" ]; then
    convert_all
    exit 0
fi

# Convert specified files
for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "Warning: File not found: $file"
        continue
    fi

    # Check file extension
    extension="${file##*.}"
    extension=$(echo "$extension" | tr '[:upper:]' '[:lower:]')

    if [ "$extension" == "m4a" ] || [ "$extension" == "wav" ]; then
        convert_file "$file"
    else
        echo "Warning: Unsupported file format: $file (only m4a and wav supported)"
    fi
done

echo "Script completed!"
