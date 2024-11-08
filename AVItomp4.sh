#!/bin/bash
# Convert AVI files to mp4
# chmod +x AVItomp4.sh
# ./AVItomp4.sh

for file in *.AVI; do
    ffmpeg -i "$file" -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k "${file%.AVI}.mp4"
done
