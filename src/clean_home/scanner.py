# TODO: Implement filesystem scan (read-only).
# - Use pathlib.Path.rglob("*") or os.walk
# - Collect FileInfo dicts
# - Mark hidden files/dirs (name startswith ".")
# - Handle permission errors (try/except, log + continue)
#
# def scan(root_path: str) -> list[dict]:
#     """Return list of FileInfo dicts (no filtering)."""
#     ...

import os
import logging
from pathlib import Path
from datetime import datetime
from fnmatch import fnmatch

# Directories to ignore
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def _should_ignore_file(file_path, exclude_patterns):
    """Checks if a file matches any exclusion pattern."""
    for pattern in exclude_patterns:
        if fnmatch(file_path.name, pattern):
            return True
    return False


def _is_eligible(file_path: Path, min_size_bytes: int, cutoff_time: datetime) -> bool:
    """Check the file depending on the criteria and age"""

    try:
        stat_info = file_path.stat()
        modified_time = datetime.fromtimestamp(stat_info.st_mtime)

        # check difference in size
        # check difference in age
        # Convert timestamp (seconds since epoch) to datetime object
        if stat_info.st_size > min_size_bytes and modified_time < cutoff_time:
            return True

    except OSError as e:
        logging.warning(
            f"Permission error or file access issue for {file_path}: {e}")
        return False

    return False


def scan_directory(root_dir: Path, min_size_bytes: int, cutoff_time: datetime, exclude_patterns: list) -> tuple[list[Path], dict]:
    """Walks the directory and finds eligible files."""
    eligible_files = []
    summary = {'total_files': 0, 'total_size': 0}
    scan_count = 0

    for root, dirs, files in os.walk(root_dir):
        current_path = Path(root)

        # Ignoring hidden/denied directories
        dirs[:] = [
            d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]

        for file_name in files:
            file_path = current_path / file_name
            scan_count += 1

            # Simple progress logging if we have multiple files
            if scan_count % 1000 == 0:
                logging.info(
                    f"Scanning... {scan_count} files inspected so far.")

            # Skip excluded files
            if _should_ignore_file(file_path, exclude_patterns):
                continue
            try:
                # Get stats for summary
                stat_info = file_path.stat()
                summary['total_files'] += 1
                summary['total_size'] += stat_info.st_size

                if _is_eligible(file_path, min_size_bytes, cutoff_time):
                    eligible_files.append(file_path)
            except FileNotFoundError:
                # File was deleted between os.walk listing and stat() call
                logging.warning(
                    f"File disappeared during scan (skipping): {file_path}")

            except OSError as e:
                # Handles PermissionError and other generic OS issues
                logging.warning(f"Error accessing {file_path}: {e}")

    return eligible_files, summary
