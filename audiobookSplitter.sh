#!/bin/bash

# chmod +x audiobookSplitter.sh

# --- Config ---
#!/bin/bash

INPUT="yourbook.m4b"
COVER="cover.jpg"
OUTPUT_DIR="chapters"
PREFIX="Meditation_"

mkdir -p "$OUTPUT_DIR"

# Extract chapter start times and titles
chapter_data=$(ffprobe -loglevel error -i "$INPUT" -show_chapters -of csv=p=0 | cut -d ',' -f 6,7)

# Put data into arrays manually
times=()
titles=()
while IFS="," read -r start title; do
    times+=("$start")
    titles+=("$title")
done <<< "$chapter_data"

# Append total duration for end time of last chapter
duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT")
times+=("$duration")

# Loop and extract
for ((i = 0; i < ${#titles[@]}; i++)); do
    start_time="${times[$i]}"
    end_time="${times[$((i + 1))]}"
    raw_title="${titles[$i]}"
    clean_title=$(echo "$raw_title" | sed 's/[^a-zA-Z0-9]/_/g' | sed 's/__/_/g' | sed 's/^_//' | sed 's/_$//')

    output_file="$OUTPUT_DIR/${PREFIX}$(printf "%02d" $i)_$clean_title.m4a"

    # For the last chapter, use duration instead of end time to avoid timing issues
    if [ $i -eq $((${#titles[@]} - 1)) ]; then
        # Last chapter - extract from start to end of file
        if [ -f "$COVER" ]; then
            ffmpeg -hide_banner -loglevel error -y \
              -ss "$start_time" -i "$INPUT" -i "$COVER" \
              -map 0:a -map 1:v \
              -c:a copy -c:v copy -disposition:v:0 attached_pic \
              -metadata title="$raw_title" \
              "$output_file"
        else
            ffmpeg -hide_banner -loglevel error -y \
              -ss "$start_time" -i "$INPUT" \
              -c copy \
              -metadata title="$raw_title" \
              "$output_file"
        fi
    else
        # Regular chapter with specific end time
        if [ -f "$COVER" ]; then
            ffmpeg -hide_banner -loglevel error -y \
              -ss "$start_time" -to "$end_time" -i "$INPUT" -i "$COVER" \
              -map 0:a -map 1:v \
              -c:a copy -c:v copy -disposition:v:0 attached_pic \
              -metadata title="$raw_title" \
              "$output_file"
        else
            ffmpeg -hide_banner -loglevel error -y \
              -ss "$start_time" -to "$end_time" -i "$INPUT" \
              -c copy \
              -metadata title="$raw_title" \
              "$output_file"
        fi
    fi

    echo "✅ Created: $output_file"
done
