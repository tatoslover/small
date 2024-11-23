#!/bin/bash
# chmod +x DownloadAudio.sh
# ./DownloadAudio.sh

# This script downloads the best audio from a video (YouTube, Vimeo, etc.),
# splits it by chapters (if available), and converts the audio to MP3 format using yt-dlp.

# Define the video URL (replace with your Vimeo video URL)
VIDEO_URL="https://player.vimeo.com/video/798208660?h=4babf25e9c&badge=0&autopause=0&player_id=0&app_id=58479"

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
