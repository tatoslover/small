#!/bin/bash

# ========================================
# AVI to MP4 Batch Converter
# ========================================
# 
# Description:
#   Converts all AVI files in the current directory to MP4 format using FFmpeg.
#   Uses H.264 video codec with CRF 22 for balanced quality/size, and AAC audio
#   codec with 192k bitrate. Original AVI files are preserved.
#
# Dependencies:
#   - FFmpeg (must be installed and in PATH)
#
# Usage:
#   chmod +x AVItomp4.sh
#   ./AVItomp4.sh
#
# Technology:
#   - FFmpeg for video conversion
#   - H.264 (libx264) video encoding
#   - AAC audio encoding
#   - Bash scripting for automation
#
# ========================================

# Check if any AVI files exist
if ! ls *.AVI >/dev/null 2>&1; then
    echo "❌ No AVI files found in current directory"
    exit 1
fi

# Convert each AVI file to MP4
for file in *.AVI; do
    # Skip if file doesn't exist (in case glob doesn't match)
    [[ ! -f "$file" ]] && continue
    
    output_file="${file%.AVI}.mp4"
    
    # Skip if output file already exists
    if [[ -f "$output_file" ]]; then
        echo "⚠️  Skipping $file - output file already exists"
        continue
    fi
    
    echo "🔄 Converting: $file -> $output_file"
    
    # Convert with error handling
    if ffmpeg -hide_banner -loglevel error -i "$file" -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k "$output_file"; then
        echo "✅ Successfully converted: $output_file"
    else
        echo "❌ Failed to convert: $file"
    fi
done

echo "🎉 Conversion process completed!"
