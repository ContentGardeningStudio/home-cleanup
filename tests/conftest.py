import pytest
from datetime import datetime, timedelta
from pathlib import Path

# --- Fixture for File Eligibility Criteria ---


@pytest.fixture
def eligibility_criteria():
    """Returns a tuple: (MIN_SIZE_BYTES, CUTOFF_TIME)"""
    MIN_SIZE_MB = 100
    MIN_SIZE_BYTES = MIN_SIZE_MB * 1024 * 1024
    CUTOFF_TIME = datetime.now() - timedelta(days=30)
    return MIN_SIZE_BYTES, CUTOFF_TIME

# --- Fixture for File Action Tests (I/O) ---


@pytest.fixture
def move_setup(tmp_path: Path):
    """
    Sets up temporary files and directories for testing file actions.
    Uses Pytest's built-in tmp_path for automatic cleanup.
    """
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    move_to_dir = tmp_path / "archive"

    # Create two dummy files with different properties
    old_large_file = source_dir / "old_large.dat"
    small_new_file = source_dir / "small_new.txt"

    # File 1: Large (200MB)
    old_large_file.write_bytes(b'0' * (200 * 1024 * 1024))

    # File 2: Small (1KB)
    small_new_file.write_bytes(b'1' * 1024)

    eligible_files = [old_large_file, small_new_file]

    # Yield the necessary setup variables
    yield eligible_files, move_to_dir, source_dir
