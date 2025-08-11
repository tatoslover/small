#!/usr/bin/osascript -l JavaScript

/**
 * Update Apple Music Play Counts Script
 *
 * This script reads a CSV file with track information and play counts,
 * finds each track in Apple Music, and plays it from near the end to
 * register a play count. It asks for confirmation between each track.
 *
 * Usage:
 *   osascript -l JavaScript update_apple_music_plays.js [path/to/csv]
 *
 * CSV format:
 *   Play Count,Track,Artist,Album,Spotify URI
 */

"use strict";

// ======= Configuration =======
const DEFAULT_CSV_PATH = "spotify_play_counts.csv";
const SKIP_TO_END_BUFFER = 5; // seconds before the end of the track
const WAIT_AFTER_PLAY = 2; // seconds to wait after track ends
const MAX_PLAYS_PER_TRACK = 1000; // increased limit to handle all real-world play counts
const DEBUG_MODE = true; // set to true to enable detailed logging

// ======= Utilities =======
function readCSVFile(filePath) {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  try {
    // Check if file exists
    const fileManager = $.NSFileManager.defaultManager;
    const fileExists = fileManager.fileExistsAtPath(filePath);

    if (!fileExists) {
      console.log(`File not found: ${filePath}`);
      return null;
    }

    // Read and parse the CSV file
    const fileContents = app.read(Path(filePath));
    const lines = fileContents.split("\n");

    // Extract header and data
    const header = lines[0].split(",");
    const data = [];

    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim() === "") continue;

      // Handle commas within quoted fields
      let values = [];
      let insideQuotes = false;
      let currentValue = "";

      for (let j = 0; j < lines[i].length; j++) {
        const char = lines[i][j];

        if (char === '"') {
          insideQuotes = !insideQuotes;
        } else if (char === "," && !insideQuotes) {
          values.push(currentValue);
          currentValue = "";
        } else {
          currentValue += char;
        }
      }

      values.push(currentValue); // Add the last value

      // Create an object with header keys
      const obj = {};
      for (let j = 0; j < header.length && j < values.length; j++) {
        obj[header[j]] = values[j].replace(/^"(.*)"$/, "$1"); // Remove surrounding quotes
      }

      data.push(obj);
    }

    return data;
  } catch (error) {
    console.log(`Error reading CSV: ${error}`);
    return null;
  }
}

function askForConfirmation(message) {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  try {
    const result = app.displayDialog(message, {
      buttons: ["Stop", "Continue", "Skip"],
      defaultButton: "Continue",
      cancelButton: "Stop",
      withIcon: "note",
    });

    return result.buttonReturned;
  } catch (error) {
    return "Stop";
  }
}

function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  let result = "";
  if (hours > 0) result += `${hours}h `;
  if (minutes > 0) result += `${minutes}m `;
  result += `${secs}s`;

  return result.trim();
}

// ======= Apple Music Control =======
function findAndPlayTrack(trackName, artistName) {
  try {
    const iTunes = Application("Music");
    iTunes.includeStandardAdditions = true;

    if (DEBUG_MODE) {
      console.log("Music application status:");
      console.log(`Running: ${iTunes.running()}`);
      console.log(`Version: ${iTunes.version()}`);
      try {
        console.log(`Current track: ${iTunes.currentTrack?.name() || "None"}`);
      } catch (e) {
        console.log(`Error getting current track: ${e}`);
      }
    }

    // First make sure Music is running
    if (!iTunes.running()) {
      iTunes.activate();
      delay(2); // Give it time to start
    }

    // Try several approaches to find tracks in the library
    let allTracks = [];
    let searchResults = [];

    // First try to get all tracks from all playlists
    console.log(
      "Searching for tracks across all your playlists and library...",
    );

    // Get list of all playlists for reference
    const allPlaylists = iTunes.playlists();
    console.log(`Found ${allPlaylists.length} playlists in total`);

    // Try to find a library playlist - try different possible names
    const libraryPlaylistNames = [
      "Library",
      "Music",
      "My Music",
      "All Music",
      "Songs",
    ];
    let libraryPlaylist = null;

    for (const name of libraryPlaylistNames) {
      try {
        const playlist = iTunes.playlists.byName(name);
        if (playlist) {
          console.log(
            `Found playlist "${name}" with ${playlist.tracks.length} tracks`,
          );
          libraryPlaylist = playlist;
          allTracks = playlist.tracks;
          break;
        }
      } catch (e) {
        // Ignore errors, try next name
      }
    }

    // If we couldn't find a library playlist, collect tracks from all playlists
    if (!libraryPlaylist) {
      console.log(
        "Could not find main library playlist, collecting tracks from all playlists",
      );
      for (let i = 0; i < allPlaylists.length; i++) {
        try {
          const playlist = allPlaylists[i];
          const playlistTracks = playlist.tracks;
          console.log(
            `Adding ${playlistTracks.length} tracks from "${playlist.name()}"`,
          );
          allTracks = allTracks.concat(playlistTracks);
        } catch (e) {
          // Skip playlists that cause errors
        }
      }
    }

    console.log(`Total tracks to search through: ${allTracks.length}`);

    // Filter tracks manually by name and artist
    let foundTrack = null;
    console.log(
      `Searching for "${trackName}" by "${artistName}" in your library...`,
    );

    if (DEBUG_MODE) {
      // List all playlists to verify we're accessing the library
      console.log("Available playlists:");
      const allPlaylists = iTunes.playlists();
      for (let i = 0; i < allPlaylists.length; i++) {
        console.log(`${i}: ${allPlaylists[i].name()}`);
      }

      console.log("Library access check:");
      try {
        console.log(`Library track count: ${allTracks.length}`);
      } catch (e) {
        console.log(`Error accessing library: ${e}`);
      }
    }

    // Loop through all tracks and find matches
    for (let i = 0; i < allTracks.length; i++) {
      try {
        const track = allTracks[i];
        const name = track.name();
        const artist = track.artist();

        // Check for partial match in both track name and artist
        if (
          name.toLowerCase().includes(trackName.toLowerCase()) ||
          trackName.toLowerCase().includes(name.toLowerCase())
        ) {
          // If artist also matches or we don't have any results yet, add to results
          if (
            artist.toLowerCase().includes(artistName.toLowerCase()) ||
            artistName.toLowerCase().includes(artist.toLowerCase())
          ) {
            searchResults.push(track);
            // If it's an exact match, use it immediately
            if (name.toLowerCase() === trackName.toLowerCase()) {
              foundTrack = track;
              break;
            }
          }
        }
      } catch (e) {
        // Skip any tracks that cause errors
        continue;
      }

      // Limit search to first 1000 tracks for performance
      if (i >= 1000) {
        console.log("Reached track limit, stopping search");
        break;
      }
    }

    console.log(`Found ${searchResults.length} potential matches`);

    // If we haven't found an exact match but have search results, use the first one
    if (!foundTrack && searchResults.length > 0) {
      foundTrack = searchResults[0];
      console.log(
        `Using best match: "${foundTrack.name()}" by "${foundTrack.artist()}"`,
      );
    }

    if (DEBUG_MODE && searchResults.length > 0) {
      console.log("Top search results:");
      const maxToShow = Math.min(5, searchResults.length);
      for (let i = 0; i < maxToShow; i++) {
        const track = searchResults[i];
        console.log(
          `${i}: "${track.name()}" by "${track.artist()}" from "${track.album()}"`,
        );
      }
    }

    if (!foundTrack) {
      return {
        success: false,
        message: `Track not found: "${trackName}" by ${artistName}. Try adding it to your library first.`,
      };
    }

    // Get track details
    const trackDuration = foundTrack.duration();
    if (DEBUG_MODE) {
      console.log("Found track details:");
      console.log(`Name: ${foundTrack.name()}`);
      console.log(`Artist: ${foundTrack.artist()}`);
      console.log(`Album: ${foundTrack.album()}`);
      console.log(`Duration: ${trackDuration} seconds`);
      try {
        console.log(`ID: ${foundTrack.id()}`);
        console.log(`Database ID: ${foundTrack.databaseID()}`);
      } catch (e) {
        console.log(`Error getting track IDs: ${e}`);
      }
    }

    // Safer approach: Use the track ID directly
    let trackID;
    try {
      trackID = foundTrack.persistentID();
    } catch (e) {
      trackID = foundTrack.id();
    }

    // Make sure playback is stopped before we start
    try {
      iTunes.stop();
      delay(1);
    } catch (e) {
      console.log(`Warning: Could not stop playback: ${e}`);
    }

    // Simplified approach - add one play
    try {
      // Play the track directly by ID if possible
      iTunes.play(foundTrack);
      delay(1); // Wait a bit to ensure it starts playing

      // Check if it's actually playing
      const isPlaying = iTunes.playerState() === "playing";
      if (!isPlaying) {
        console.log("Warning: Track didn't start playing, trying again...");
        iTunes.play(foundTrack);
        delay(1);
      }

      // Skip to near the end
      const skipToPosition = Math.max(1, trackDuration - SKIP_TO_END_BUFFER);
      iTunes.playerPosition = skipToPosition;

      // Wait for the track to finish
      const timeToWait = SKIP_TO_END_BUFFER + WAIT_AFTER_PLAY;
      delay(timeToWait);

      // Stop playback
      iTunes.stop();
      delay(0.5);

      return {
        success: true,
        message: `Played "${foundTrack.name()}" by ${foundTrack.artist()}`,
        track: {
          name: foundTrack.name(),
          artist: foundTrack.artist(),
          album: foundTrack.album(),
          duration: trackDuration,
          id: trackID,
        },
      };
    } catch (playError) {
      console.log(`Error during playback: ${playError}`);

      // Try to recover
      try {
        iTunes.stop();
      } catch (e) {
        // Ignore stop errors
      }

      return {
        success: false,
        message: `Error playing track: ${playError}`,
        recoverable: true,
      };
    }
  } catch (error) {
    if (DEBUG_MODE) {
      console.log("Detailed error information:");
      console.log(`Error type: ${typeof error}`);
      console.log(`Error message: ${error.message || error}`);
      console.log(`Error stack: ${error.stack || "No stack available"}`);

      // Try to get more information about the current state
      try {
        const iTunes = Application("Music");
        console.log(`Music app running: ${iTunes.running()}`);
        console.log(`Current player state: ${iTunes.playerState()}`);
      } catch (e) {
        console.log(`Additional error during diagnostics: ${e}`);
      }
    }

    return {
      success: false,
      message: `Error accessing Music app: ${error}`,
      recoverable: false,
    };
  }
}
// Previously replaced

// ======= Main Function =======
function main() {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  try {
    // Print operating environment info in debug mode
    if (DEBUG_MODE) {
      console.log("=== DEBUG INFORMATION ===");
      try {
        console.log(
          `OS Version: ${$.NSProcessInfo.processInfo.operatingSystemVersionString}`,
        );
        console.log(`User Name: ${$.NSUserName()}`);
        console.log(`Home Directory: ${$.NSHomeDirectory()}`);
        console.log(
          `Current Directory: ${$.NSFileManager.defaultManager.currentDirectoryPath}`,
        );
      } catch (e) {
        console.log(`Error getting system info: ${e}`);
      }
      console.log("=========================\n");
    }

    // Get arguments
    const args = $.NSProcessInfo.processInfo.arguments;
    const csvPath =
      args.count > 4 ? ObjC.unwrap(args.objectAtIndex(4)) : DEFAULT_CSV_PATH;

    console.log(`Reading CSV from: ${csvPath}`);
    const tracks = readCSVFile(csvPath);

    if (!tracks || tracks.length === 0) {
      console.log("No tracks found in CSV file.");
      return;
    }

    console.log(`Found ${tracks.length} tracks in CSV file.`);

    // Initialize counters
    let totalTracksProcessed = 0;
    let totalPlaysAdded = 0;
    let skippedTracks = 0;
    let notFoundTracks = 0;

    // Process each track
    for (let i = 0; i < tracks.length; i++) {
      try {
        // Reset the Music app between tracks to avoid state issues
        try {
          const iTunes = Application("Music");
          iTunes.stop();
          delay(1);
        } catch (e) {
          console.log(`Warning: Could not reset Music app: ${e}`);
        }

        const track = tracks[i];
        const trackName = track["Track"];
        const artistName = track["Artist"];
        let playCount = parseInt(track["Play Count"]);

        // Safety check for play count
        if (isNaN(playCount) || playCount <= 0) {
          console.log(
            `Skipping "${trackName}" - Invalid play count: ${track["Play Count"]}`,
          );
          skippedTracks++;
          continue;
        }

        // Limit to MAX_PLAYS_PER_TRACK to avoid excessive runs
        if (playCount > MAX_PLAYS_PER_TRACK) {
          console.log(
            `Limiting plays for "${trackName}" from ${playCount} to ${MAX_PLAYS_PER_TRACK}`,
          );
          playCount = MAX_PLAYS_PER_TRACK;
        }

        // Prepare full track identification for confirmation
        let trackDetails = `"${trackName}" by ${artistName}`;
        if (track["Album"]) {
          trackDetails += ` from album "${track["Album"]}"`;
        }

        console.log(
          `\nTrack ${i + 1}/${tracks.length}: "${trackName}" by ${artistName}`,
        );
        console.log(`Target plays: ${playCount}`);

        // Ask for confirmation before starting this track
        const confirmMessage =
          `Ready to process track ${i + 1}/${tracks.length}:\n` +
          trackDetails +
          `\n\n` +
          `This will add ${playCount} plays to Apple Music WITHOUT interruption.\n\n` +
          `Progress: ${totalPlaysAdded} plays added, ${notFoundTracks} tracks not found, ` +
          `${skippedTracks} tracks skipped.`;

        const response = askForConfirmation(confirmMessage);

        if (response === "Stop") {
          console.log("User chose to stop processing.");
          break;
        } else if (response === "Skip") {
          console.log(`Skipping "${trackName}" by ${artistName}`);
          skippedTracks++;
          continue;
        }

        // Add plays
        let successfulPlays = 0;
        let consecutiveErrors = 0;
        const MAX_CONSECUTIVE_ERRORS = 3;

        for (let j = 0; j < playCount; j++) {
          console.log(`Adding play ${j + 1}/${playCount} for "${trackName}"`);

          const result = findAndPlayTrack(trackName, artistName);

          if (result.success) {
            console.log(`✓ ${result.message}`);
            successfulPlays++;
            totalPlaysAdded++;
            consecutiveErrors = 0; // Reset error counter on success
          } else {
            console.log(`✗ ${result.message}`);

            if (j === 0) {
              notFoundTracks++;
              break; // Skip this track entirely if first play fails
            }

            consecutiveErrors++;

            // If this is a recoverable error, try again after a short pause
            if (
              result.recoverable &&
              consecutiveErrors < MAX_CONSECUTIVE_ERRORS
            ) {
              console.log(
                `Recoverable error, pausing for 5 seconds before retry...`,
              );
              delay(5);
              j--; // Retry this play count
              continue;
            }

            // Too many consecutive errors, skip remaining plays for this track
            if (consecutiveErrors >= MAX_CONSECUTIVE_ERRORS) {
              console.log(
                `Too many consecutive errors (${consecutiveErrors}), skipping remaining plays for this track`,
              );
              break;
            }
          }

          // No confirmation between plays of the same track
          // Slightly longer delay between plays to reduce errors
          delay(1.5);
        }

        if (successfulPlays > 0) {
          totalTracksProcessed++;

          // Show a summary after completing all plays for this track
          if (i < tracks.length - 1) {
            // If this isn't the last track
            const trackSummaryMessage =
              `Added ${successfulPlays} plays for "${trackName}" by ${artistName}.\n\n` +
              `Ready to continue to the next track?`;

            const continueResponse = askForConfirmation(trackSummaryMessage);

            if (continueResponse === "Stop") {
              console.log("User chose to stop processing.");
              break;
            }
          }
        }
      } catch (trackError) {
        console.log(`Error processing track: ${trackError}`);
        // Continue with next track
      }
    }

    // Show final results
    const summaryMessage =
      `Play count update complete!\n\n` +
      `Tracks processed: ${totalTracksProcessed}/${tracks.length}\n` +
      `Plays added: ${totalPlaysAdded}\n` +
      `Tracks not found: ${notFoundTracks}\n` +
      `Tracks skipped: ${skippedTracks}`;

    app.displayDialog(summaryMessage, {
      buttons: ["OK"],
      defaultButton: "OK",
      withIcon: "note",
    });
  } catch (error) {
    console.log(`Error in main: ${error}`);
  }
}

// Run the script
main();
