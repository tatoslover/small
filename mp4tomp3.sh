#!/bin/bash
# Convert mp4 files to mp3
# chmod +x mp4tomp3.sh
# ./mp4tomp3.sh

# Loop through all mp4 files in the current directory
for file in *.mp4; do
  # Extract the base name without extension
  base_name="${file%.*}"
  # Convert the mp4 file to mp3
  ffmpeg -i "$file" -ab 320k "${base_name}.mp3"
done
