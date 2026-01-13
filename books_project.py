#!/usr/bin/env python3

# ========================================
# Book Collection to Obsidian Notes Generator
# ========================================
#
# Description:
#   Converts a CSV file containing book collection data into individual Markdown files
#   for Obsidian vault. Each book gets its own note with YAML front matter and structured
#   template including sections for summary, key takeaways, quotes, and personal notes.
#
# Dependencies:
#   - pandas (pip install pandas)
#   - Python 3.6+
#
# Usage:
#   1. Ensure your Books.csv file is in the correct location
#   2. Update file paths below to match your system
#   3. cd "/Users/samuellove/Library/Mobile Documents/com~apple~CloudDocs/Zed"
#   4. python books_project.py
#
# Technology:
#   - Pandas for CSV data processing
#   - Regular expressions for filename sanitization
#   - YAML front matter for metadata
#   - Template-based markdown generation
#   - File system operations for Obsidian integration
#
# CSV Format Expected:
#   Columns: Title, Series, Author, Genre, Year Read, Rating
#
# Output:
#   Individual .md files in Obsidian Books vault with structured templates
#   ready for personal notes and knowledge management.
#
# ========================================


# Path to your downloaded CSV file and target folder
books = "/Users/samuellove/Library/Mobile Documents/com~apple~Numbers/Documents/Books.csv"
obsidian_books = "/Users/samuellove/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/Books"

    sys.exit(1)


    print(f"❌ Error creating output directory: {e}")
    sys.exit(1)

# Load CSV file into DataFrame
try:
    df = pd.read_csv(books)
    print(f"📊 Loaded {len(df)} books from CSV file")
except Exception as e:
    print(f"❌ Error reading CSV file: {e}")
    sys.exit(1)

# Validate required columns exist
required_columns = ['Title', 'Author', 'Year Read', 'Rating']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"❌ Error: Missing required columns: {missing_columns}")
    print(f"Available columns: {list(df.columns)}")
    sys.exit(1)

# Template for new files
template = """---
Title: {title}
Series: {series}
Author: {author}
Genre: {genre}
Years:
  - "{years_read}"
Rating: {rating}
---

## Summary

Provide a brief summary or synopsis of the book here.

## Key Takeaways

- **Key Point 1**: Description
- **Key Point 2**: Description

## Quotes

Include notable quotes from the book.

> "Quote from the book."

## Notes

Write any additional notes or reflections about the book.
"""

# Function to sanitize file names
def sanitize_filename(filename):
    if not filename or not filename.strip():
        return "Untitled"
    # Remove invalid characters and limit length
    clean_name = re.sub(r'[\/:*?"<>|]', '', str(filename).strip())
    # Ensure filename isn't too long (most filesystems limit to 255 chars)
    return clean_name[:200] if len(clean_name) > 200 else clean_name

# Process each book
success_count = 0
error_count = 0

for index, row in df.iterrows():  # Use df.head(2) to limit to first 2 rows
    try:
        # Handle missing or NaN values
        title = str(row.get('Title', 'Untitled')).strip()
        series = str(row.get('Series', '')).strip()
        author = str(row.get('Author', 'Unknown')).strip()
        genre = str(row.get('Genre', 'Unknown')).strip()
        years_read = str(row.get('Year Read', '')).strip()
        rating = str(row.get('Rating', '')).strip()

        # Skip rows with empty titles
        if not title or title.lower() == 'nan':
            print(f"⚠️  Skipping row {index + 1}: No title provided")
            continue

        file_content = template.format(
            title=title,
            series=series,
            author=author,
            genre=genre,
            years_read=years_read,
            rating=rating
        )



        # Write file content to new file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_content)

        error_count += 1
        print(f"❌ Error processing row {index + 1} ('{title}'): {e}")

print(f"\n🎉 Book note generation completed!")
print(f"📊 Summary: {success_count} notes created, {error_count} errors")
