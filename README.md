# Small Scripts Collection 🛠️

A curated collection of utility scripts for media conversion, content organization, and workflow automation. Each script is designed to solve specific everyday tasks with minimal setup and maximum efficiency.

## 📁 Scripts Overview

### 🎬 Media Conversion & Processing

#### `AVItomp4.sh`
**Purpose**: Batch convert AVI video files to MP4 format
- **Technology**: FFmpeg, H.264 encoding, AAC audio
- **Use Case**: Modernizing old video files for better compatibility
- **Features**: Quality optimization (CRF 22), fast preset, error handling
- **Usage**: `./AVItomp4.sh` (processes all .AVI files in current directory)

#### `mp4tomp3.sh`
**Purpose**: Extract high-quality audio from MP4 video files
- **Technology**: FFmpeg, 320kbps MP3 encoding
- **Use Case**: Creating audio libraries from video content
- **Features**: Batch processing, original file preservation, duplicate detection
- **Usage**: `./mp4tomp3.sh` (processes all .mp4 files in current directory)

#### `audiobookSplitter.sh`
**Purpose**: Split audiobook files into individual chapters with embedded cover art
- **Technology**: FFmpeg, chapter metadata parsing, image embedding
- **Use Case**: Converting monolithic audiobooks into organized chapter files
- **Features**: Automatic chapter detection, cover art embedding, metadata preservation
- **Usage**: Configure INPUT and COVER variables, then run `./audiobookSplitter.sh`

### 📥 Content Download & Extraction

#### `DownloadAudio.sh`
**Purpose**: Download and extract audio from YouTube/Vimeo with chapter splitting
- **Technology**: yt-dlp, FFmpeg, chapter detection
- **Use Case**: Creating podcast/music libraries from video content
- **Features**: Automatic chapter splitting, fallback logic, MP3 conversion
- **Usage**: Edit VIDEO_URL variable, then run `./DownloadAudio.sh`

#### `download_vids.sh`
**Purpose**: Download entire YouTube playlists at optimized quality
- **Technology**: yt-dlp, quality filtering (720p max)
- **Use Case**: Archiving educational content, tutorials, or entertainment
- **Features**: Playlist indexing, organized naming, directory management
- **Usage**: Edit PLAYLIST_URL variable, then run `./download_vids.sh`

### 📚 Knowledge Management & Organization

#### `bookmarks.py`
**Purpose**: Convert Safari bookmarks to individual Markdown files with metadata
- **Technology**: BeautifulSoup, YAML front matter, regex sanitization
- **Use Case**: Integrating bookmarks with note-taking systems (Obsidian, etc.)
- **Features**: Category preservation, duplicate handling, error recovery
- **Usage**: Export Safari bookmarks as HTML, then run `python bookmarks.py`

#### `books_project.py`
**Purpose**: Generate Obsidian notes from book collection CSV data
- **Technology**: Pandas, template generation, YAML front matter
- **Use Case**: Creating structured book review system in Obsidian
- **Features**: Templated note structure, metadata integration, batch processing
- **Usage**: Configure CSV path, then run `python books_project.py`

#### `generate_html_notes.sh`
**Purpose**: Create structured HTML learning notes for W3Schools tutorials
- **Technology**: Bash arrays, dynamic folder creation, markdown templates
- **Use Case**: Organizing web development learning materials
- **Features**: Hierarchical structure, overview generation, Obsidian integration
- **Usage**: Configure VAULT_PATH, then run `./generate_html_notes.sh`

### 🗂️ File Management & Organization

#### `rename_comics.sh`
**Purpose**: Clean up comic book filenames by removing metadata clutter
- **Technology**: sed regex, batch file operations
- **Use Case**: Organizing digital comic collections
- **Features**: Pattern-based cleaning, collision detection, safe renaming
- **Usage**: Navigate to comic directory, then run `./rename_comics.sh`

## 🚀 Quick Start

### Prerequisites

```bash
# Install required tools
brew install ffmpeg  # For media scripts
pip install yt-dlp beautifulsoup4 pandas  # For download and conversion scripts
```

### Basic Usage Pattern

1. **Make scripts executable**:
   ```bash
   chmod +x *.sh
   ```

2. **Configure variables** in scripts as needed (URLs, paths, etc.)

3. **Run in target directory** where files are located

4. **Check output** for success/error messages

## 🛡️ Safety Features

All scripts include:
- ✅ **File existence validation**
- ✅ **Duplicate detection and handling**
- ✅ **Error reporting with clear messages**
- ✅ **Original file preservation**
- ✅ **Progress indicators and status updates**

## 📋 Dependencies Summary

| Script | Dependencies | Installation |
|--------|-------------|-------------|
| `AVItomp4.sh` | FFmpeg | `brew install ffmpeg` |
| `mp4tomp3.sh` | FFmpeg | `brew install ffmpeg` |
| `audiobookSplitter.sh` | FFmpeg | `brew install ffmpeg` |
| `DownloadAudio.sh` | yt-dlp, FFmpeg | `pip install yt-dlp` |
| `download_vids.sh` | yt-dlp | `pip install yt-dlp` |
| `bookmarks.py` | BeautifulSoup4 | `pip install beautifulsoup4` |
| `books_project.py` | Pandas | `pip install pandas` |
| `generate_html_notes.sh` | None (bash built-ins) | - |
| `rename_comics.sh` | None (sed, mv) | - |

## 💡 Use Cases & Workflows

### 🎓 Learning & Knowledge Management
- Export Safari bookmarks → Convert to Markdown → Import to Obsidian
- CSV book data → Structured notes → Personal library system
- Tutorial organization → Hierarchical folders → Study materials

### 🎵 Media Library Creation
- YouTube playlists → Downloaded videos → Audio extraction → Music library
- Audiobooks → Chapter splitting → Organized library
- Old video files → Format conversion → Modern compatibility

### 🗃️ Content Organization
- Comic collections → Filename cleanup → Organized library
- Video downloads → Quality optimization → Storage efficiency

## 🔧 Customization

Most scripts can be easily customized by editing variables at the top:

- **File paths**: Update directory locations for your system
- **Quality settings**: Modify FFmpeg parameters for different output quality
- **Naming patterns**: Adjust filename templates and sanitization rules
- **URL targets**: Change download sources and playlists

## 📝 Contributing

To add new scripts to this collection:

1. Follow the established header format with description, dependencies, and usage
2. Include error handling and user feedback
3. Add safety checks for file operations
4. Update this README with script description
5. Test thoroughly before committing

## 🐛 Troubleshooting

### Common Issues

**FFmpeg not found**: Install with `brew install ffmpeg` or your package manager

**yt-dlp errors**: Update with `pip install --upgrade yt-dlp`

**Permission denied**: Make scripts executable with `chmod +x scriptname.sh`

**No files found**: Ensure you're in the directory containing target files

**Python module errors**: Install dependencies with `pip install module_name`

## 📄 License

These scripts are provided as-is for personal and educational use. Modify and distribute freely.

---

*This collection represents practical solutions to common digital content management challenges. Each script emphasizes automation, safety, and user feedback for reliable everyday use.*