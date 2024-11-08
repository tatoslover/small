#!/bin/bash
# cd '/Users/samuellove/Library/Mobile Documents/com~apple~CloudDocs/Zed'
# chmod +x YoutubeAudio.sh
# ./YoutubeAudio.sh

# This script downloads the best audio from a YouTube video, splits it by chapters,
# and converts the audio files to MP3 format using yt-dlp.

# Define the YouTube video URL
VIDEO_URL="https://www.youtube.com/watch?v=0cKzCUdtRh8&t=1822s"

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
