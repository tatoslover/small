#!/usr/bin/env python3
"""
Apple Music Automation Preparation Script

This script takes your spotify_play_counts.csv and creates a scaled-down version
that's more suitable for automation with Apple Shortcuts.

Usage:
    python prepare_apple_music_automation.py [--input INPUT_CSV] [--output OUTPUT_CSV]
                                             [--limit TRACK_LIMIT] [--max-plays MAX_PLAYS]
"""


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Prepare Spotify play count data for Apple Music automation')
    parser.add_argument('--input', default='spotify_play_counts.csv',
                        help='Path to input CSV file (default: spotify_play_counts.csv)')
    parser.add_argument('--output', default='apple_music_automation.csv',
                        help='Path to output CSV file (default: apple_music_automation.csv)')
    parser.add_argument('--limit', type=int, default=100,
                        help='Maximum number of tracks to include (default: 100)')
    parser.add_argument('--max-plays', type=int, default=10,
                        help='Maximum plays per track (default: 10)')
    parser.add_argument('--scale', action='store_true',
                        help='Scale play counts proportionally instead of capping')
    return parser.parse_args()

def read_csv(file_path):


    tracks = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tracks.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    return tracks

def scale_play_counts(tracks, max_plays, use_scaling=False):
    """Scale or cap play counts for each track."""

    if not tracks:
        return []

    # Convert play counts to integers
    for track in tracks:
        track['Play Count'] = int(track['Play Count'])

    # Sort by play count (descending)
    tracks.sort(key=lambda x: x['Play Count'], reverse=True)

    if use_scaling:
        # Find the maximum play count
        max_count = tracks[0]['Play Count']

        # Calculate scaling factor
        scale_factor = max_plays / max_count

        # Scale all play counts, ensuring minimum of 1 play if original count > 0
        for track in tracks:
            original_count = track['Play Count']
            if original_count > 0:
                scaled_count = max(1, round(original_count * scale_factor))
                track['Original Play Count'] = original_count
                track['Play Count'] = scaled_count
    else:
        # Cap play counts at max_plays
        for track in tracks:
            original_count = track['Play Count']
            capped_count = min(original_count, max_plays)
            if original_count > max_plays:
                track['Original Play Count'] = original_count
            track['Play Count'] = capped_count

    return tracks

def write_csv(tracks, output_file, limit):
    """Write the processed tracks to a new CSV file."""
    # Limit the number of tracks
    limited_tracks = tracks[:limit]

    # Calculate statistics
    total_original_plays = sum(int(track.get('Original Play Count', track['Play Count'])) for track in limited_tracks)
    total_scaled_plays = sum(int(track['Play Count']) for track in limited_tracks)

    # Write to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Determine fieldnames based on whether we have original counts
            if 'Original Play Count' in limited_tracks[0]:
                fieldnames = ['Play Count', 'Original Play Count', 'Track', 'Artist', 'Album', 'Spotify URI']
            else:
                fieldnames = ['Play Count', 'Track', 'Artist', 'Album', 'Spotify URI']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for track in limited_tracks:
                writer.writerow(track)

        print(f"Successfully wrote {len(limited_tracks)} tracks to {output_file}")
        print(f"Original total plays: {total_original_plays}")
        print(f"Scaled total plays: {total_scaled_plays}")
        print(f"Reduction: {total_original_plays - total_scaled_plays} plays ({(1 - total_scaled_plays/total_original_plays)*100:.1f}%)")

        # Calculate approximate time
        seconds_per_play = 11  # 5 seconds of the song + 6 seconds wait
        total_seconds = total_scaled_plays * seconds_per_play
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        print(f"Estimated automation time: {hours} hours, {minutes} minutes")

        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False

def main():
    """Main function."""
    args = parse_args()

    print(f"Reading play counts from {args.input}...")
    tracks = read_csv(args.input)

    if not tracks:
        return

    print(f"Processing {len(tracks)} tracks...")
    print(f"{'Scaling' if args.scale else 'Capping'} play counts to maximum {args.max_plays} plays per track")
    processed_tracks = scale_play_counts(tracks, args.max_plays, args.scale)

    print(f"Limiting to top {args.limit} tracks...")
    write_csv(processed_tracks, args.output, args.limit)

    print("\nNext steps:")
    print("1. Use this CSV file with the JXA script:")
    print(f"   osascript -l JavaScript update_apple_music_plays.js {args.output}")
    print("2. The script will add the specified number of plays for each track")
    print("3. This will take time, but you can control the pace with confirmation prompts")

if __name__ == "__main__":
    main()
