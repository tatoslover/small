#!/usr/bin/osascript -l JavaScript

// Simple test script to verify Apple Music access
// Run with: osascript -l JavaScript test_apple_music.js

'use strict';

// Helper function to display a dialog
function showDialog(message) {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;

  try {
    app.displayDialog(message, {
      buttons: ["OK"],
      defaultButton: "OK",
      withIcon: "note"
    });
  } catch (error) {
    console.log(`Failed to show dialog: ${error}`);
  }
}

// Run a series of tests to check Apple Music access
function runTests() {
  console.log("Starting Apple Music access tests...");
  const results = [];

  try {
    // Test 1: Can we access the Music app?
    const iTunes = Application("Music");
    iTunes.includeStandardAdditions = true;
    results.push(`1. Music app access: SUCCESS`);
    results.push(`   Version: ${iTunes.version()}`);
    results.push(`   Running: ${iTunes.running()}`);

    // Test 2: Can we get playlists?
    const playlists = iTunes.playlists();
    results.push(`2. Found ${playlists.length} playlists: SUCCESS`);
    results.push(`   First 5 playlists: ${playlists.slice(0, 5).map(p => p.name()).join(", ")}`);

    // Test 3: Can we access the main library?
    const libraryPlaylist = iTunes.libraryPlaylists["Library"];
    results.push(`3. Library access: SUCCESS`);
    results.push(`   Library name: ${libraryPlaylist.name()}`);

    // Test 4: Can we get tracks from the library?
    const tracks = libraryPlaylist.tracks;
    results.push(`4. Library tracks: SUCCESS`);
    results.push(`   Found ${tracks.length} tracks in library`);

    if (tracks.length > 0) {
      // Test 5: Can we get track details?
      const sampleTrack = tracks[0];
      results.push(`5. Track details: SUCCESS`);
      results.push(`   Sample track: "${sampleTrack.name()}" by "${sampleTrack.artist()}"`);
      results.push(`   Album: ${sampleTrack.album()}`);
      results.push(`   Duration: ${sampleTrack.duration()} seconds`);

      // Test 6: Can we search for tracks?
      const searchTerm = sampleTrack.name().split(" ")[0]; // Use first word of track name
      const searchResults = libraryPlaylist.searchFor(searchTerm, { only: "songs" });
      results.push(`6. Search functionality: SUCCESS`);
      results.push(`   Search for "${searchTerm}" found ${searchResults.length} results`);

      // Test 7: Can we play a track?
      try {
        iTunes.play(sampleTrack);
        delay(1); // Wait 1 second
        const isPlaying = iTunes.playerState() === "playing";
        iTunes.stop();
        results.push(`7. Play track: ${isPlaying ? "SUCCESS" : "FAILED"}`);
      } catch (e) {
        results.push(`7. Play track: FAILED - ${e}`);
      }
    }

    // Success summary
    console.log("All tests completed!");
    const allResults = results.join("\n");
    console.log(allResults);

    // Show results in a dialog
    showDialog(`Apple Music Access Test Results:\n\n${allResults}`);

  } catch (error) {
    console.log(`Test failed: ${error}`);
    showDialog(`Test failed: ${error}\n\nPartial results:\n${results.join("\n")}`);
  }
}

// Run the tests
runTests();
