# bookmarks
# cd "/Users/samuellove/Library/Mobile Documents/com~apple~CloudDocs/Zed"
# python bookmarks.py

import os
from bs4 import BeautifulSoup
import re

# Function to sanitize file names
def sanitize_filename(filename):
    # Remove invalid characters for file names (like slashes, colons, etc.)
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Open and read the exported Safari bookmarks HTML file
with open("Safari Bookmarks.html", "r") as file:
    html = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Directory where the markdown files will be saved
output_directory = "Bookmarks"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Dictionary to keep track of categories
current_category = ""

# Extract all links and convert each bookmark to its own markdown file with YAML front matter
for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a"]):
    if element.name.startswith('h'):  # If the element is a header
        current_category = element.text.strip()
    elif element.name == "a":  # If the element is a link
        title = element.text.strip()
        url = element["href"]

        # Sanitize the title to create a valid file name
        file_name = sanitize_filename(f"{title}.md")

        # Prepare the content for the markdown file with YAML front matter
        yaml_content = f"""---
Title: "{title}"
Link: "{url}"
Category: "{current_category}"
---

"""

        # Write the content to a new markdown file in the output directory
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, "w") as file:
            file.write(yaml_content)

        print(f"Created: {file_name}")

print("All bookmarks have been converted to individual markdown files with YAML front matter!")
