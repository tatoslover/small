#!/usr/bin/env python3
"""
Spotify Play Count Processor

This script processes Spotify streaming history data and generates play count statistics.

Usage:
    python spotify_to_apple_music.py

The script will:
1. Parse Spotify streaming history JSON files
2. Count plays for each track
3. Generate a CSV report with play count data
4. Create a top tracks summary report

import glob
from collections import defaultdict

class SpotifyPlayCounter:
    def __init__(self, data_dir="data"):
        """
        Initialize the Spotify Play Counter processor.

        Args:
            data_dir (str): Directory containing Spotify streaming history JSON files
        """
        self.data_dir = data_dir
        self.history_files = []
        self.track_plays = defaultdict(int)
        self.track_data = {}
        self.min_play_threshold_ms = 30000  # Minimum 30 seconds to count as a play

        # Current folder for all files
        self.support_folder = "."


            print(f"No streaming history files found in {self.data_dir}")
            return False
        print(f"Found {len(self.history_files)} streaming history files.")
        return True

    def process_history_files(self):
        """Process all Spotify streaming history files."""
        total_tracks = 0
        valid_plays = 0

                    data = json.load(file)

                    for entry in data:
                        total_tracks += 1

                        # Skip podcast episodes and audiobooks
                        if entry.get('episode_name') or entry.get('audiobook_title'):
                            continue

                        # Skip entries with insufficient play time
                        if entry.get('ms_played', 0) < self.min_play_threshold_ms:
                            continue

                        track_name = entry.get('master_metadata_track_name')
                        artist_name = entry.get('master_metadata_album_artist_name')
                        album_name = entry.get('master_metadata_album_album_name')

                        # Skip entries with missing track or artist info
                        if not track_name or not artist_name:
                            continue

                        # Create a unique key for the track
                        track_key = f"{artist_name} - {track_name}"

                        # Increment play count
                        self.track_plays[track_key] += 1
                        valid_plays += 1

                        # Store track data if not already stored
                        if track_key not in self.track_data:
                            self.track_data[track_key] = {
                                'track_name': track_name,
                                'artist_name': artist_name,
                                'album_name': album_name,
                                'spotify_uri': entry.get('spotify_track_uri', '')
                            }
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        print(f"Processed {total_tracks} total entries, found {valid_plays} valid plays for {len(self.track_plays)} unique tracks.")

    def generate_report(self, output_file="spotify_play_counts.csv"):
        """
        Generate a CSV report with play count data.

        Args:
            output_file (str): Path to output CSV file
        """
        if not self.track_plays:
            print("No play data to report. Run process_history_files first.")
            return

        # Sort tracks by play count (descending)
        sorted_tracks = sorted(self.track_plays.items(), key=lambda x: x[1], reverse=True)

            fieldnames = ['Play Count', 'Track', 'Artist', 'Album', 'Spotify URI']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for track_key, play_count in sorted_tracks:
                track_info = self.track_data[track_key]
                writer.writerow({
                    'Play Count': play_count,
                    'Track': track_info['track_name'],
                    'Artist': track_info['artist_name'],
                    'Album': track_info['album_name'],
                    'Spotify URI': track_info['spotify_uri']
                })

        print(f"Report generated: {output_path}")



    def generate_top_tracks_report(self, output_file="top_tracks.txt", count=50):
        """
        Generate a plain text report with top tracks by play count.

        Args:
            output_file (str): Path to output text file
            count (int): Number of top tracks to include
        """
        if not self.track_plays:
            print("No play data available. Run process_history_files first.")
            return

            file.write(f"TOP {count} TRACKS BY PLAY COUNT\n")
            file.write("=" * (count + 22) + "\n\n")

            # Sort tracks by play count (descending)
            sorted_tracks = sorted(self.track_plays.items(), key=lambda x: x[1], reverse=True)

            # List top tracks
            for i, (track_key, play_count) in enumerate(sorted_tracks[:count]):
                if i >= count:
                    break
                track_info = self.track_data[track_key]
                file.write(f"{i+1}. {track_info['track_name']} by {track_info['artist_name']} - {play_count} plays\n")

        print(f"Top tracks report generated: {output_path}")



    def run(self):
        """Run the Spotify play count processor."""
        print("Starting Spotify play count processor...")

                print(f"Warning: Could not create support folder: {e}")

        if self.find_history_files():
            self.process_history_files()
            self.generate_report()
            self.generate_top_tracks_report()

            print("\nProcess completed successfully!")
            print("Your files have been saved:")
            print("- spotify_play_counts.csv - Complete play count data")
            print("- top_tracks.txt - Summary of your top tracks")
            print("\nTo update Apple Music play counts:")
            print("- Run: osascript -l JavaScript update_apple_music_plays.js")
            print("\nIf you have many tracks with high play counts:")
            print("- First run: python prepare_apple_music_automation.py")
        else:
            print("Process failed. No streaming history files found.")


if __name__ == "__main__":
    processor = SpotifyPlayCounter()
    processor.run()
