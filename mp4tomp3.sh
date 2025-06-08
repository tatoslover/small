#!/bin/bash

# ========================================
# MP4 to MP3 Batch Converter
# ========================================
# 
# Description:
#   Converts all MP4 video files in the current directory to high-quality MP3 audio files.
#   Uses FFmpeg with 320k bitrate for excellent audio quality. Original MP4 files are preserved.
#   Perfect for extracting audio from video files for music libraries or podcasts.
#
# Dependencies:
#   - FFmpeg (must be installed and in PATH)
#
# Usage:
#   chmod +x mp4tomp3.sh
#   ./mp4tomp3.sh
#
# Technology:
#   - FFmpeg for audio extraction and conversion
#   - 320k bitrate for high-quality MP3 output
#   - Bash scripting for batch processing
#   - File extension manipulation for naming
#
# Note:
#   This script preserves original MP4 files and creates new MP3 files with
#   the same base filename in the current directory.
#
# ========================================

# Check if any MP4 files exist
if ! ls *.mp4 >/dev/null 2>&1; then
    echo "❌ No MP4 files found in current directory"
    exit 1
fi

# Loop through all mp4 files in the current directory
for file in *.mp4; do
  # Skip if file doesn't exist (in case glob doesn't match)
  [[ ! -f "$file" ]] && continue
  
  # Extract the base name without extension
  base_name="${file%.*}"
  output_file="${base_name}.mp3"
  
  # Skip if output file already exists
  if [[ -f "$output_file" ]]; then
      echo "⚠️  Skipping $file - output file already exists"
      continue
  fi
  
  echo "🔄 Converting: $file -> $output_file"
  
  # Convert the mp4 file to mp3 with error handling
  if ffmpeg -hide_banner -loglevel error -i "$file" -ab 320k "$output_file"; then
      echo "✅ Successfully converted: $output_file"
  else
      echo "❌ Failed to convert: $file"
  fi
done

echo "🎉 Conversion process completed!"
