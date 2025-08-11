# Spotify to Apple Music Play Count Transfer

This project helps you analyze your Spotify streaming history and transfer your play counts to Apple Music. 

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Getting Your Spotify Data](#getting-your-spotify-data)
  - [Setup Instructions](#setup-instructions)
- [Basic Usage](#basic-usage)
- [Understanding the Output Files](#understanding-the-output-files)
- [Updating Apple Music Play Counts](#updating-apple-music-play-counts)
  - [Using the JXA Script](#using-the-jxa-script)
  - [How the JXA Script Works](#how-the-jxa-script-works)
  - [For Large Libraries](#for-large-libraries)
- [Customization](#customization)
- [Notes and Limitations](#notes-and-limitations)

## Overview

This toolkit consists of multiple components that work together:

1. **Main Script (`spotify_to_apple_music.py`)**: 
   - Processes your Spotify streaming history
   - Counts plays for each track (filtering out podcasts, etc.)
   - Generates CSV report and top tracks summary

2. **JXA Script (`update_apple_music_plays.js`)**:
   - Uses JavaScript for Automation to interact with Apple Music
   - Searches for your tracks in Apple Music
   - Plays them from near the end to register play counts
   - Interactive interface with confirmation prompts

3. **Preparation Script (`prepare_apple_music_automation.py`)**:
   - Creates scaled-down versions of your play count data
   - Useful for large libraries with many high-count tracks

All files are contained within this single folder for simplicity.

## Getting Started

### Getting Your Spotify Data

1. Go to your [Spotify Account Privacy Settings](https://www.spotify.com/account/privacy/)
2. Request your data by clicking "Request" under "Download your data"
3. Wait for Spotify to process your request (can take up to 30 days, but typically less)
4. Download the ZIP file when it's ready
5. Extract the files and locate the streaming history JSON files (named like `Streaming_History_Audio_YYYY_X.json`)

### Setup Instructions

1. Place your Spotify streaming history JSON files in the `data` directory (already included)
2. Make sure the scripts are executable:
   ```
   chmod +x spotify_to_apple_music.py
   chmod +x update_apple_music_plays.js
   ```

## Basic Usage

Run the main script:

```
python spotify_to_apple_music.py
```

The script will:
- Find all Spotify streaming history JSON files in the `data` directory
- Process and analyze your streaming history
- Generate two output files:
  - `spotify_play_counts.csv` - A CSV file with all your play counts
  - `top_tracks.txt` - A simple text file listing your top 50 tracks

## Understanding the Output Files

### spotify_play_counts.csv

This CSV file contains detailed information about all your played tracks:
- **Play Count** - Number of times you played the track
- **Track** - Track name
- **Artist** - Artist name
- **Album** - Album name
- **Spotify URI** - Spotify's unique identifier for the track

### top_tracks.txt

A simple text file with your top 50 most played tracks, showing:
- Ranking
- Track name
- Artist name
- Number of plays

## Updating Apple Music Play Counts

Apple Music doesn't provide a direct API to update play counts. However, play counts are incremented when a track finishes playing. We can use this behavior to update play counts by playing tracks from near the end.

### Using the JXA Script

1. Run the JXA script:
   ```
   osascript -l JavaScript update_apple_music_plays.js
   ```
   
2. The script will:
   - Read your `spotify_play_counts.csv` file
   - For each track, ask for your confirmation before processing
   - Find the track in Apple Music and play it from near the end
   - Ask for confirmation again before each additional play
   - Display a summary when finished

3. Interactive Controls:
   - **Continue**: Process the current track/play
   - **Skip**: Skip the current track/play and move to the next one
   - **Stop**: Stop the entire process

4. Handling Missing Tracks:
   - If the script can't find a track, it will tell you it's missing
   - You can add these tracks to your Apple Music library manually
   - After adding missing tracks, run the script again to process them

### How the JXA Script Works

1. The script searches for each track in Apple Music using the track name and artist
2. When found, it plays the track and immediately skips to a few seconds before the end
3. It waits for the track to finish, which registers a play count in Apple Music
4. This process repeats for each track according to its play count
5. You have control between each play with confirmation prompts

### For Large Libraries

If you have many tracks with high play counts, the process can take a long time. Use the preparation script to create a more manageable version:

```
python prepare_apple_music_automation.py
```

Options:
- `--input` - Path to input CSV (default: `spotify_play_counts.csv`)
- `--output` - Path to output CSV (default: `apple_music_automation.csv`)
- `--limit` - Maximum number of tracks to include (default: 100)
- `--max-plays` - Maximum plays per track (default: 10)
- `--scale` - Scale play counts proportionally instead of capping

After creating the scaled-down version, run the JXA script with this file:

```
osascript -l JavaScript update_apple_music_plays.js apple_music_automation.csv
```

## Customization

You can modify these parameters in the scripts:

In `spotify_to_apple_music.py`:
- `min_play_threshold_ms` - Minimum milliseconds to count as a play (default: 30000)
- Count of top tracks to include in report (default: 50)

In `update_apple_music_plays.js`:
- `SKIP_TO_END_BUFFER` - Seconds before the end to start playing (default: 5)
- `WAIT_AFTER_PLAY` - Seconds to wait after track ends (default: 2)

## Notes and Limitations

- The script considers a valid play as any track played for at least 30 seconds
- Podcast episodes and audiobooks are excluded from the play count statistics
- The JXA script will update play counts in Apple Music, but the plays will be recorded on the current date, not distributed over time like your original Spotify history
- The match between Spotify and Apple Music tracks isn't always perfect - some tracks might not be found
- The process takes time - each play requires about 7-10 seconds
- You can stop the JXA script at any time and resume later
- The JXA script does not limit play counts and will add the exact number of plays from your Spotify data

## Troubleshooting

### Missing Tracks
If the script can't find specific tracks:
1. Open Apple Music and search for the missing track
2. Add it to your library (click the "+" button)
3. Run the script again - it should now find the track

### Track Matching
The script searches your Apple Music library for tracks with similar names and artists to your Spotify data. If tracks aren't being found:
1. Check that the tracks exist in your Apple Music library
2. Consider that track names might be slightly different between Spotify and Apple Music
3. For tracks with very different names, you may need to manually update the CSV file

### Permissions
The script needs permission to control Apple Music:
1. When prompted, allow the script to control the Music app
2. If no prompt appears but the script doesn't work, check System Preferences → Security & Privacy → Automation