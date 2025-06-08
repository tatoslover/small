#!/bin/bash

# ========================================
# One Piece Comics Batch Filename Cleaner
# ========================================
# 
# Description:
#   Cleans up One Piece comic book (.cbz) filenames by removing unwanted metadata
#   like publication years, digital release tags, and release group identifiers.
#   Designed specifically for One Piece comic collection organization.
#
# Dependencies:
#   - Standard Unix tools (sed, mv)
#   - Comic files in CBZ format
#
# Usage:
#   1. Navigate to your One Piece comics directory
#   2. cd /Users/samuellove/Documents/Comics/One_Piece
#   3. chmod +x rename_comics.sh
#   4. ./rename_comics.sh
#
# Technology:
#   - Bash scripting for batch file operations
#   - sed with extended regular expressions for pattern matching
#   - File system operations for renaming
#
# Patterns Removed:
#   - Publication years: " (2023)", " (1999)", etc.
#   - Digital release tags: " (Digital) (1r0n) (f)"
#   - Other metadata formatting inconsistencies
#
# ========================================

# Check if any CBZ files exist
if ! ls *.cbz >/dev/null 2>&1; then
    echo "❌ No CBZ comic files found in current directory"
    exit 1
fi

for f in *.cbz; do
    # Skip if file doesn't exist (in case glob doesn't match)
    [[ ! -f "$f" ]] && continue
    
    # Use sed to remove the year and other unwanted parts
    newname=$(echo "$f" | sed -E 's/ \([0-9]{4}\)//g' | sed -E 's/ \(Digital\) \(1r0n\) \(f\)//g')
    
    # Skip if the filename wouldn't change
    if [[ "$f" == "$newname" ]]; then
        echo "⚠️  Skipping $f - no changes needed"
        continue
    fi
    
    # Skip if target file already exists
    if [[ -f "$newname" ]]; then
        echo "⚠️  Skipping $f - target file already exists: $newname"
        continue
    fi
    
    echo "🔄 Renaming: $f -> $newname"
    
    # Rename the file with error handling
    if mv "$f" "$newname"; then
        echo "✅ Successfully renamed: $newname"
    else
        echo "❌ Failed to rename: $f"
    fi
done

echo "🎉 Comic renaming process completed!"
