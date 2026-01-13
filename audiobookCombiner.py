#!/usr/bin/env python3
"""
Audiobook Combiner - Merge multiple audio files into a single audiobook
Requires: ffmpeg (install via: brew install ffmpeg)
"""

import os
import sys
import subprocess
from pathlib import Path


def get_audio_files(directory: str) -> list[Path]:
    """Get all audio files from directory, sorted naturally"""
    audio_extensions = {".mp3", ".m4a", ".m4b", ".aac", ".wav", ".flac", ".ogg"}
    files = [
        f for f in Path(directory).iterdir() if f.suffix.lower() in audio_extensions
    ]
    return sorted(files, key=lambda x: x.name)


def create_file_list(audio_files: list[Path], list_file: str = "filelist.txt") -> str:
    """Create a text file listing all audio files for ffmpeg concat"""
    with open(list_file, "w") as f:
        for audio_file in audio_files:
            safe_path = str(audio_file.absolute()).replace("'", "'\\''")
            _ = f.write(f"file '{safe_path}'\n")
    return list_file


def find_cover_image(directory: str) -> str | None:
    """Find a cover image in the directory"""
    image_extensions = {".jpg", ".jpeg", ".png"}
    common_names = ["cover", "folder", "front", "album"]

    dir_path = Path(directory)

    # First, look for common cover image names
    for name in common_names:
        for ext in image_extensions:
            for path in dir_path.glob(f"{name}*{ext}"):
                return str(path.absolute())
            for path in dir_path.glob(f"{name.upper()}*{ext}"):
                return str(path.absolute())

    # If not found, just return the first image file
    for ext in image_extensions:
        images = list(dir_path.glob(f"*{ext}"))
        if images:
            return str(images[0].absolute())

    return None


def combine_audiobook(
    input_dir: str,
    output_file: str,
    metadata: dict[str, str] | None = None,
    cover_image: str | None = None,
) -> tuple[bool, str]:
    """Combine audio files into a single audiobook

    Args:
        input_dir: Directory containing audio files to combine
        output_file: Path where the combined audiobook will be saved
        metadata: Optional dictionary with keys like 'title', 'author', 'album'
        cover_image: Optional path to cover image file

    Returns:
        Tuple of (success_flag, message)
    """
    """Combine audio files into a single audiobook"""

    # Get all audio files
    audio_files = get_audio_files(input_dir)

    if not audio_files:
        return False, "No audio files found in directory"

    print(f"\nFound {len(audio_files)} audio files:")
    for f in audio_files:
        print(f"  - {f.name}")

    # Create file list for ffmpeg
    list_file = create_file_list(audio_files)

    # Build ffmpeg command
    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file]

    # Add cover image if provided
    if cover_image and os.path.exists(cover_image):
        print(f"Adding cover image: {Path(cover_image).name}")
        cmd.extend(["-i", cover_image])
        cmd.extend(["-map", "0:a", "-map", "1:v", "-c:a", "copy"])

        # For M4B/M4A files, use AAC video codec for cover
        if output_file.lower().endswith((".m4b", ".m4a")):
            cmd.extend(["-c:v", "png"])  # Keep as PNG for M4B
        else:
            cmd.extend(["-c:v", "copy"])

        cmd.extend(["-disposition:v:0", "attached_pic"])
    else:
        cmd.extend(["-c", "copy"])

    # Add metadata if provided
    if metadata:
        if metadata.get("title"):
            cmd.extend(["-metadata", f"title={metadata['title']}"])
        if metadata.get("author"):
            cmd.extend(["-metadata", f"artist={metadata['author']}"])
        if metadata.get("album"):
            cmd.extend(["-metadata", f"album={metadata['album']}"])

    cmd.append(output_file)

    print(f"\nCombining into: {output_file}")
    print("Processing...")
    print(f"\nRunning command: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check if output file was actually created and has content
        if not os.path.exists(output_file):
            if os.path.exists(list_file):
                os.remove(list_file)
            return False, f"Output file was not created. ffmpeg error:\n{result.stderr}"

        file_size = os.path.getsize(output_file)
        if file_size == 0:
            if os.path.exists(list_file):
                os.remove(list_file)
            if os.path.exists(output_file):
                os.remove(output_file)
            return False, f"Output file is empty. ffmpeg error:\n{result.stderr}"

        # Check return code
        if result.returncode != 0:
            if os.path.exists(list_file):
                os.remove(list_file)
            return False, f"ffmpeg failed with error:\n{result.stderr}"

        # Clean up
        if os.path.exists(list_file):
            os.remove(list_file)

        size_mb = file_size / (1024 * 1024)
        return True, f"Successfully created: {output_file}\nSize: {size_mb:.1f} MB"

    except subprocess.CalledProcessError as e:
        if os.path.exists(list_file):
            os.remove(list_file)
        error_output = e.stderr if hasattr(e, "stderr") and e.stderr else str(e)
        return False, f"Error combining files: {error_output}"
    except FileNotFoundError:
        if os.path.exists(list_file):
            os.remove(list_file)
        return False, "ffmpeg not found. Install it with: brew install ffmpeg"


def select_folder_gui():
    """Use AppleScript to show a native folder picker"""
    script = """
    tell application "System Events"
        activate
        set folderPath to choose folder with prompt "Select the folder containing your audiobook files:"
        return POSIX path of folderPath
    end tell
    """

    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def select_file_gui(prompt: str, file_types: list[str] | None = None) -> str | None:
    """Use AppleScript to show a native file picker"""
    if file_types:
        types_str = ", ".join([f'"{t}"' for t in file_types])
        type_clause = f"of type {{{types_str}}}"
    else:
        type_clause = ""

    script = f'''
    tell application "System Events"
        activate
        set filePath to choose file with prompt "{prompt}" {type_clause}
        return POSIX path of filePath
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_input_gui(prompt: str, default: str = "") -> str | None:
    """Use AppleScript to show a native input dialog"""
    script = f'''
    tell application "System Events"
        activate
        set userInput to text returned of (display dialog "{prompt}" default answer "{default}")
        return userInput
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def show_message_gui(title: str, message: str, msg_type: str = "information") -> None:
    """Use AppleScript to show a native message dialog"""
    icon = "note" if msg_type == "information" else "stop"
    script = f'''
    tell application "System Events"
        activate
        display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK" with icon {icon}
    end tell
    '''

    _ = subprocess.run(["osascript", "-e", script], capture_output=True)


def ask_yes_no_gui(prompt: str) -> bool:
    """Use AppleScript to show a native yes/no dialog"""
    script = f'''
    tell application "System Events"
        activate
        set response to button returned of (display dialog "{prompt}" buttons {{"No", "Yes"}} default button "No")
        return response
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        return result.stdout.strip() == "Yes"
    except subprocess.CalledProcessError:
        return False


def main_gui():
    """GUI mode using native macOS dialogs"""
    print("Starting Audiobook Combiner (GUI mode)...")

    # Select folder
    print("Please select a folder...")
    input_dir = select_folder_gui()

    if not input_dir:
        print("Cancelled by user")
        return

    # Check for audio files
    audio_files = get_audio_files(input_dir)

    if not audio_files:
        show_message_gui(
            "No Audio Files", "No audio files found in the selected directory.", "stop"
        )
        return

    # Show file count
    folder_name = Path(input_dir).name
    default_output = f"{folder_name}_combined.m4b"

    # Get output filename
    output_file = get_input_gui(
        f"Found {len(audio_files)} audio files.\\n\\nEnter output filename:",
        default_output,
    )

    if not output_file:
        print("Cancelled by user")
        return

    # Ensure output has extension
    if not Path(output_file).suffix:
        output_file += ".m4b"

    # Make output path relative to input directory
    output_path = str(Path(input_dir) / output_file)

    # Ask about metadata
    add_metadata = ask_yes_no_gui(
        "Would you like to add metadata (title, author, album)?"
    )

    metadata: dict[str, str] = {}
    if add_metadata:
        title = get_input_gui("Enter title (or leave blank):", "")
        if title:
            metadata["title"] = title

        author = get_input_gui("Enter author (or leave blank):", "")
        if author:
            metadata["author"] = author

        album = get_input_gui("Enter album/series (or leave blank):", "")
        if album:
            metadata["album"] = album

    # Check for cover image
    auto_cover = find_cover_image(input_dir)
    cover_image = None

    if auto_cover:
        use_auto_cover = ask_yes_no_gui(
            f"Found cover image: {Path(auto_cover).name}\\n\\nUse this image?"
        )
        if use_auto_cover:
            cover_image = auto_cover
        else:
            select_custom = ask_yes_no_gui(
                "Would you like to select a different cover image?"
            )
            if select_custom:
                cover_image = select_file_gui("Select cover image", ["public.image"])
    else:
        select_cover = ask_yes_no_gui(
            "No cover image found.\\n\\nWould you like to select one?"
        )
        if select_cover:
            cover_image = select_file_gui("Select cover image", ["public.image"])

    # Combine the files
    meta_to_use = metadata if metadata else None
    success, message = combine_audiobook(
        input_dir, output_path, meta_to_use, cover_image
    )

    if success:
        show_message_gui("Success", message, "information")
    else:
        show_message_gui("Error", message, "stop")


def main_cli():
    """CLI mode (original interactive mode)"""
    print("=== Audiobook Combiner ===\n")

    # Get input directory
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = input("Enter the directory containing audio files: ").strip()

    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a valid directory")
        sys.exit(1)

    # Get output filename
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        default_name = f"{Path(input_dir).name}_combined.m4b"
        output_file = input(f"Enter output filename [{default_name}]: ").strip()
        if not output_file:
            output_file = default_name

    # Ensure output has extension
    if not Path(output_file).suffix:
        output_file += ".m4b"

    # Make output path relative to input directory
    output_path = str(Path(input_dir) / output_file)

    # Optional metadata
    add_metadata_response = input("\nAdd metadata? (y/n) [n]: ").strip().lower()
    add_metadata = add_metadata_response
    metadata: dict[str, str] = {}

    if add_metadata == "y":
        title = input("Title: ").strip()
        if title:
            metadata["title"] = title

        author = input("Author: ").strip()
        if author:
            metadata["author"] = author

        album = input("Album/Series: ").strip()
        if album:
            metadata["album"] = album

    # Check for cover image
    cover_image = None
    auto_cover = find_cover_image(input_dir)

    if auto_cover:
        use_cover = (
            input(
                f"\nFound cover image: {Path(auto_cover).name}\nUse this? (y/n) [y]: "
            )
            .strip()
            .lower()
        )
        if use_cover != "n":
            cover_image = auto_cover
        else:
            custom_path = input("Enter path to cover image (or leave blank): ").strip()
            if custom_path and os.path.exists(custom_path):
                cover_image = custom_path
    else:
        custom_path = input("\nEnter path to cover image (or leave blank): ").strip()
        if custom_path and os.path.exists(custom_path):
            cover_image = custom_path

    # Combine the files
    meta_to_use = metadata if metadata else None
    success, message = combine_audiobook(
        input_dir, output_path, meta_to_use, cover_image
    )

    _ = print(f"\n{message}")
    sys.exit(0 if success else 1)


def main():
    # Check if CLI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] in ["--cli", "-c"]:
        _ = sys.argv.pop(1)  # Remove the flag
        main_cli()
    elif len(sys.argv) > 1:
        # If arguments provided, use CLI mode
        main_cli()
    else:
        # No arguments, use GUI mode
        main_gui()


if __name__ == "__main__":
    main()
