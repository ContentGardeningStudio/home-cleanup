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


def scan_directory(root_dir: Path, min_size_bytes: int, cutoff_time: datetime, exclude_patterns: list) -> tuple[list[Path], dict]:
    """Walks the directory and finds eligible files."""
    eligible_files = []
    summary = {'total_files': 0, 'total_size': 0}
