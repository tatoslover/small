#!/bin/bash

# Set your vault location here (change path as needed)
VAULT_PATH="/Users/samuellove/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/NZSL"
# Create main NZSL folder
mkdir -p "$VAULT_PATH"

# Vocabulary categories
VOCAB=("Numbers" "Alphabet" "Colours" "Food" "Drinks" "Animals" "Nature" "Travel" "People" "Family" "Clothing" "Technology" "Health" "Emotions" "Work" "Sports" "Time" "Weather" "Hobbies")
for v in "${VOCAB[@]}"; do
    mkdir -p "$VAULT_PATH/Vocabulary/$v"
done

# Grammar topics
GRAMMAR=("Sentence Structure" "Questions" "Negation" "Classifiers" "Tense" "Directionality" "Non-Manual Signals" "Verbs" "Adjectives" "Plurality")
for g in "${GRAMMAR[@]}"; do
    mkdir -p "$VAULT_PATH/Grammar/$g"
done

# Culture & history
CULTURE=("Deaf Culture" "Deaf History" "Deaf Etiquette" "Famous Deaf People" "NZSL Week")
for c in "${CULTURE[@]}"; do
    mkdir -p "$VAULT_PATH/Culture/$c"
done

# Practice & immersion
PRACTICE=("Daily Logs" "Meetup Notes" "Practice Videos" "Conversation Practice" "Games")
for p in "${PRACTICE[@]}"; do
    mkdir -p "$VAULT_PATH/Practice/$p"
done

# Templates
mkdir -p "$VAULT_PATH/Templates"
cat <<EOT > "$VAULT_PATH/Templates/Daily_Sign_Log.md"
# Daily Sign Log - {{date}}

**Signs Learned Today:**
1.
2.
3.

**Example Sentences:**
-
-

**Practice Notes:**
-

**Links to NZSL Dictionary:**
-

---
EOT

cat <<EOT > "$VAULT_PATH/Templates/Vocab_Note_Template.md"
# {{sign_name}}

**Category:**
**Handshape:**
**Movement:**
**Location:**
**Palm Orientation:**
**Non-Manual Signals:**

**Video Link:**
- [NZSL Dictionary Search](https://www.nzsl.nz/)

**Example Sentence:**
-

---
EOT

echo "✅ NZSL learning folder structure created at: $VAULT_PATH"
