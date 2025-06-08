#!/bin/bash

# ========================================
# YouTube/Vimeo Audio Downloader with Chapter Splitting
# ========================================
# 
# Description:
#   Downloads the best quality audio from YouTube, Vimeo, and other supported platforms.
#   Automatically detects and splits videos by chapters if available, otherwise downloads
#   the entire video as a single audio file. Converts all audio to MP3 format.
#
# Dependencies:
#   - yt-dlp (pip install yt-dlp)
#   - FFmpeg (for audio conversion)
#
# Usage:
#   1. Edit VIDEO_URL variable below with your target URL
#   2. chmod +x DownloadAudio.sh
#   3. ./DownloadAudio.sh
#
# Technology:
#   - yt-dlp for video/audio extraction
#   - FFmpeg for audio format conversion
#   - Bash scripting for automation and fallback logic
#   - Chapter detection and splitting
#
# Features:
#   - Automatic chapter detection and splitting
#   - Fallback to full audio if no chapters found
#   - MP3 conversion with best available quality
#   - Organized file naming with chapter numbers and titles
#
# ========================================

# Define the video URL (replace with your Vimeo video URL)
VIDEO_URL="https://www.youtube.com/watch?v=w3r2J4-QpIg"

# Define the base output directory in the Downloads folder
OUTPUT_DIR="$HOME/Downloads/%(title)s"

# Use yt-dlp to download the video, saving to the specified output path
yt-dlp --split-chapters -f bestaudio --extract-audio --audio-format mp3 -o "$OUTPUT_DIR/%(chapter_number)s - %(chapter_title)s.%(ext)s" "$VIDEO_URL"

# Check if any files were created
if [ ! "$(ls -A "$OUTPUT_DIR")" ]; then
    # If no chapter files were created, download the best audio without splitting
    yt-dlp -f bestaudio --extract-audio --audio-format mp3 -o "$HOME/Downloads/%(title)s.%(ext)s" "$VIDEO_URL"
else
    # Move the chapter files to the Downloads folder if they were created elsewhere
    mv "$OUTPUT_DIR"/* "$HOME/Downloads/"
fi

# Inform the user that the download is complete
echo "Download complete! Audio files have been saved to your Downloads folder."
