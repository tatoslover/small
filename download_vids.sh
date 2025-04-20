#!/bin/bash
# chmod +x /Users/samuellove/Documents/GitHub/small/download_vids.sh
# /Users/samuellove/Documents/GitHub/small/download_vids.sh

# Set your playlist URL here
PLAYLIST_URL="https://www.youtube.com/playlist?list=PLBfRLLhSBb-DxOwxuN2yvik4mRuSJk_Qi"

# Set output directory (or leave blank for current directory)
OUTPUT_DIR="./downloads"

# Make output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Download videos at best available format up to 720p
yt-dlp \
  -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
  -o "$OUTPUT_DIR/%(playlist_index)s - %(title)s.%(ext)s" \
  --yes-playlist \
  "$PLAYLIST_URL"
