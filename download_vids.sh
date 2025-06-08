#!/bin/bash

# ========================================
# YouTube Playlist Video Downloader
# ========================================
# 
# Description:
#   Downloads all videos from a YouTube playlist at 720p quality or best available.
#   Automatically creates numbered files with playlist index and video titles.
#   Organizes downloads into a dedicated directory structure.
#
# Dependencies:
#   - yt-dlp (pip install yt-dlp)
#   - FFmpeg (for video processing)
#
# Usage:
#   1. Edit PLAYLIST_URL variable below with your target playlist
#   2. chmod +x /Users/samuellove/Documents/GitHub/small/download_vids.sh
#   3. /Users/samuellove/Documents/GitHub/small/download_vids.sh
#
# Technology:
#   - yt-dlp for video extraction and playlist handling
#   - Format selection for quality control (720p max)
#   - Bash scripting for automation
#   - File naming with playlist indexing
#
# Features:
#   - Downloads entire playlists automatically
#   - Quality limited to 720p for reasonable file sizes
#   - Organized file naming with playlist order
#   - Creates output directory if it doesn't exist
#
# ========================================

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
