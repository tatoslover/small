# books_project
# cd "/Users/samuellove/Library/Mobile Documents/com~apple~CloudDocs/Zed"
# python books_project.py

import pandas as pd
import os
import re

# Path to your downloaded CSV file and target folder
books = "/Users/samuellove/Library/Mobile Documents/com~apple~Numbers/Documents/Books.csv"
obsidian_books = "/Users/samuellove/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/Books"

# Load CSV file into DataFrame
df = pd.read_csv(books)

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
    return re.sub(r'[\/:*?"<>|]', '', filename)

# Run it
for index, row in df.iterrows():  # Use df.head(2) to limit to first 2 rows
    file_content = template.format(
        title=row['Title'],
        series=row['Series'],
        author=row['Author'],
        genre=row.get('Genre', 'Unknown'),  # Default to 'Unknown' if Genre is missing
        years_read=row['Year Read'],
        rating=row['Rating']
    )

    # Define file name and path
    file_name = f"{sanitize_filename(row['Title'])}.md"  # Sanitize the title to remove invalid characters
    file_path = os.path.join(obsidian_books, file_name)

    # Write file content to new file
    with open(file_path, 'w') as file:
        file.write(file_content)

    print(f"Created: {file_name}")
