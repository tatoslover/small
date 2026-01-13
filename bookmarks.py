#!/usr/bin/env python3

# ========================================
# Safari Bookmarks to Markdown Converter
# ========================================
#
# Description:
#   Converts exported Safari bookmarks HTML file into individual Markdown files
#   with YAML front matter. Each bookmark becomes a separate .md file organized
#   by category with metadata for easy searching and integration with note-taking apps.
#
# Dependencies:
#   - beautifulsoup4 (pip install beautifulsoup4)
#   - Python 3.6+
#
# Usage:
#   1. Export Safari bookmarks as HTML file named "Safari Bookmarks.html"
#   2. Place this script in the same directory as the HTML file
#   3. cd "/Users/samuellove/Library/Mobile Documents/com~apple~CloudDocs/Zed"
#   4. python bookmarks.py
#
# Technology:
#   - BeautifulSoup for HTML parsing
#   - Regular expressions for filename sanitization
#   - YAML front matter for metadata
#   - File system operations for organization
#
# Output:
#   Creates a "Bookmarks" directory with individual .md files for each bookmark
#   containing title, URL, and category metadata.
#


# Function to sanitize file names
def sanitize_filename(filename):
    # Remove invalid characters for file names (like slashes, colons, etc.)
    return re.sub(r'[\\/*?:"<>|]', "", filename)


    exit(1)

# Open and read the exported Safari bookmarks HTML file
try:
    with open(bookmarks_file, "r", encoding="utf-8") as file:
        html = file.read()
except Exception as e:
    print(f"❌ Error reading {bookmarks_file}: {e}")
    exit(1)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Directory where the markdown files will be saved

    print(f"❌ Error creating output directory: {e}")
    exit(1)

# Dictionary to keep track of categories
current_category = "Uncategorized"
bookmark_count = 0
error_count = 0

# Extract all links and convert each bookmark to its own markdown file with YAML front matter
for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a"]):
    if element.name.startswith('h'):  # If the element is a header
        current_category = element.text.strip() if element.text else "Uncategorized"
    elif element.name == "a":  # If the element is a link
        try:
            title = element.text.strip() if element.text else "Untitled"
            url = element.get("href", "")

            # Skip bookmarks without URLs
            if not url:
                print(f"⚠️  Skipping bookmark without URL: {title}")
                continue

            # Sanitize the title to create a valid file name
            file_name = sanitize_filename(f"{title}.md")

            # Handle duplicate or empty filenames
            if not file_name or file_name == ".md":


            # Prepare the content for the markdown file with YAML front matter
            yaml_content = f"""---
Title: "{title.replace('"', '\\"')}"
Link: "{url.replace('"', '\\"')}"
Category: "{current_category.replace('"', '\\"')}"
---

"""

            # Write the content to a new markdown file in the output directory
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(yaml_content)

            error_count += 1
            print(f"❌ Error processing bookmark '{title}': {e}")

print(f"\n🎉 Bookmark conversion completed!")
print(f"📊 Summary: {bookmark_count} bookmarks created, {error_count} errors")
