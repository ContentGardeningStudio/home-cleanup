import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from pathlib import Path

from clean_home.scanner import _is_eligible, scan_directory


def make_mock_path(size: int, age_days: int):
    """Return a MagicMock simulating a file Path with .stat()."""
    mock_path = MagicMock(spec=Path)
    mock_stat = MagicMock()
    mock_stat.st_size = size
    mock_stat.st_mtime = (
        datetime.now() - timedelta(days=age_days)).timestamp()
    mock_path.stat.return_value = mock_stat
    return mock_path

# --- Unit test of eligibilty


def test_file_eligible(eligibility_criteria):
    """Should be eligible if size exceeds threshold."""
    min_size, cutoff_time = eligibility_criteria
    path = make_mock_path(size=min_size + 1000, age_days=40)
    assert _is_eligible(path, min_size, cutoff_time) is True


def test_file_not_eligible(eligibility_criteria):
    """Should NOT be eligible if too small and too recent."""
    min_size, cutoff_time = eligibility_criteria
    path = make_mock_path(size=min_size - 1, age_days=1)
    assert _is_eligible(path, min_size, cutoff_time) is False


def test_file_access_error_handled(eligibility_criteria):
    """If stat() raises OSError, it should return False (gracefully)."""
    min_size, cutoff_time = eligibility_criteria
    mock_path = MagicMock(spec=Path)
    mock_path.stat.side_effect = OSError("Permission denied")
    assert _is_eligible(mock_path, min_size, cutoff_time) is False

# Unit test for scan directory


@pytest.mark.parametrize("exclude_patterns", [[], ["*.log"]])
def test_scan_directory_with_mocks(mocker, eligibility_criteria, exclude_patterns):
    """Test that scan_directory correctly finds eligible files and ignores excluded ones."""
    min_size, cutoff_time = eligibility_criteria

    '''Simulate a directory'''
    mocker.patch(
        "os.walk",
        return_value=[
            ("/root", ["temp", ".git"], ["a.txt", "b.log"]),
            ("/root/temp", [], ["c.txt"]),
        ]
    )
    '''Simulate file eligibility'''
    mocker.patch(
        "clean_home.scanner._is_eligible",
        return_value=[True, False, True]
    )

    '''Simulate the file size'''

    mocker.patch(
        "pathlib.Path.stat",
        side_effect=[
            MagicMock(st_size=1000),  # a.txt
            MagicMock(st_size=500),   # b.log
            MagicMock(st_size=2000),  # c.txt
        ]
    )

    # Execution
    eligible, summary = scan_directory(
        root_dir=Path("/root"),
        min_size_bytes=min_size,
        cutoff_time=cutoff_time,
        exclude_patterns=exclude_patterns
    )

    assert len(eligible) == 2  # a.txt et c.txt are eligible
    assert summary["total_files"] == 3
    assert summary["total_size"] == 3500
