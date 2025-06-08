#!/bin/bash

: <<'NOTE'
📄 Script: generate_html_notes.sh

🧰 Description:
Creates folders and markdown notes for W3Schools HTML tutorials in your Obsidian vault.
Outputs an `HTML Overview.md` file linking to each note.

🖥️ How to Use:
1. Save the file.
2. Make it executable: chmod +x generate_html_notes.sh
3. Run it: ./generate_html_notes.sh /path/to/your/vault
   (or omit the path to use the current directory)

✅ Example:
   ./generate_html_notes.sh ~/Documents/Obsidian/MyVault
NOTE

# --- Step 1: Set working directory ---
VAULT_PATH="/Users/samuellove/Library/Mobile Documents/iCloud~md~obsidian/Documents"
cd "$VAULT_PATH" || {
  echo "❌ Failed to change directory to: $VAULT_PATH"
  exit 1
}

# --- Step 2: Section names and their notes ---
section_names=(
  "HTML Tutorial"
  "HTML Forms"
  "HTML Graphics"
  "HTML Media"
  "HTML APIs"
  "HTML Examples"
)

notes_HTML_Tutorial=(
  "Introduction" "Editors" "Basic" "Elements" "Attributes" "Headings" "Paragraphs"
  "Styles" "Formatting" "Quotations" "Comments" "Colors" "CSS" "Links" "Images"
  "Favicon" "Page Title" "Tables" "Lists" "Block & Inline" "Div" "Classes" "Id"
  "Iframes" "JavaScript" "File Paths" "Head" "Layout" "Responsive" "Computercode"
  "Semantics" "Style Guide" "Entities" "Symbols" "Emojis" "Charsets" "URL Encode" "vs. XHTML"
)

notes_HTML_Forms=(
  "Forms" "Form Attributes" "Form Elements" "Input Types"
  "Input Attributes" "Input Form Attributes"
)

notes_HTML_Graphics=("Canvas" "SVG")
notes_HTML_Media=("Media" "Video" "Audio" "Plug-ins" "YouTube")
notes_HTML_APIs=("Web APIs" "Geolocation" "Drag and Drop" "Web Storage" "Web Workers" "SSE")

notes_HTML_Examples=(
  "Examples" "Editor" "Quiz" "Exercises" "Website" "Syllabus"
  "Study Plan" "Interview Prep" "Bootcamp" "Certificate" "Summary" "Accessibility"
)

# --- Step 3: Create folders and notes ---
for section in "${section_names[@]}"; do
  mkdir -p "$section"

  # Convert "HTML Tutorial" to notes_HTML_Tutorial
  var_name="notes_${section// /_}"
  eval "notes=(\"\${$var_name[@]}\")"

  for note in "${notes[@]}"; do
    note_file="$section/$note.md"
    [ ! -f "$note_file" ] && echo "# $note" > "$note_file"
  done
done

# --- Step 4: Create Overview File ---
INDEX_FILE="HTML Overview.md"
{
  echo "# HTML - W3Schools Overview"
  echo

  for section in "${section_names[@]}"; do
    case "$section" in
      "HTML Tutorial") echo "## 📘 $section" ;;
      "HTML Forms") echo "## 🧾 $section" ;;
      "HTML Graphics") echo "## 🎨 $section" ;;
      "HTML Media") echo "## 🎧 $section" ;;
      "HTML APIs") echo "## 🔌 $section" ;;
      "HTML Examples") echo "## 💡 $section" ;;
    esac

    var_name="notes_${section// /_}"
    eval "notes=(\"\${$var_name[@]}\")"

    for note in "${notes[@]}"; do
      echo "- [[${section}/${note}]]"
    done

    echo
  done
} > "$INDEX_FILE"

echo "✅ HTML tutorial note structure created at: $VAULT_PATH"
