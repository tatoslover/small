#!/bin/bash

# Adjust this to your NZSL folder inside your Obsidian vault
NZSL_PATH="/Users/samuellove/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/NZSL/Vocabulary/Common"

mkdir -p "$NZSL_PATH"

declare -A signs=(
  ["Hello"]="https://www.nzsl.nz/sign/1105/"
  ["Thank You"]="https://www.nzsl.nz/sign/209/"
  ["Yes"]="https://www.nzsl.nz/sign/1933/"
  ["No"]="https://www.nzsl.nz/sign/1803/"
  ["Please"]="https://www.nzsl.nz/sign/2359/"
  ["Sorry"]="https://www.nzsl.nz/sign/2282/"
  ["Help"]="https://www.nzsl.nz/sign/1470/"
  ["Eat"]="https://www.nzsl.nz/sign/765/"
  ["Drink"]="https://www.nzsl.nz/sign/657/"
  ["Bathroom"]="https://www.nzsl.nz/sign/2476/"
)

for sign in "${!signs[@]}"; do
  filename="${NZSL_PATH}/${sign// /_}.md"
  cat <<EOT > "$filename"
# $sign

**Category:** Common Signs

**Video link:** [NZSL Dictionary](${signs[$sign]})

**Description:**
- Meaning: $sign
- Usage notes:

**Example sentence:**
-

---
EOT
done

echo "✅ Basic NZSL sign notes created in $NZSL_PATH"
