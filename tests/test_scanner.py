import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from pathlib import Path

from clean_home.scanner import _is_eligible, scan_directory


def make_mock_path(size: int, age_days: int):
    """Return a MagicMock simulating a file Path with .stat()."""
    mock_path = MagicMock(spec=Path)
    mock_stat = MagicMock()
    mock_stat.st_size = size
    mock_stat.st_mtime = (datetime.now() - timedelta(days=age_days)).timestamp()
    mock_path.stat.return_value = mock_stat
    return mock_path


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


@pytest.mark.parametrize("exclude_patterns", [[], ["*.log"]])
def test_scan_directory_with_mocks(mocker, eligibility_criteria, exclude_patterns):
    """Test that scan_directory correctly finds eligible files and ignores excluded ones."""
    min_size, cutoff_time = eligibility_criteria

    # Simulate a directory
    mocker.patch(
        "os.walk",
        return_value=[
            ("/root", ["temp", ".git"], ["a.txt", "b.log"]),
            ("/root/temp", [], ["c.txt"]),
        ],
    )

    # Mock _is_eligible
    def fake_is_eligible(path, *_, **__):
        return Path(path).name in ("a.txt", "c.txt")

    mocker.patch("clean_home.scanner._is_eligible", side_effect=fake_is_eligible)

    # Patch Path.stat ONLY for the duration of scan_directory
    original_stat = Path.stat

    def fake_stat(self):
        sizes = {"a.txt": 1000, "b.log": 500, "c.txt": 2000}
        m = MagicMock()
        m.st_size = sizes.get(self.name, 0)
        m.st_mode = 0o100644  # valid int for pytest internal use
        return m

    mocker.patch("clean_home.scanner.Path.stat", new=fake_stat)

    # Run the function under test
    eligible, summary = scan_directory(
        root_dir=Path("/root"),
        min_size_bytes=min_size,
        cutoff_time=cutoff_time,
        exclude_patterns=exclude_patterns,
    )

    # Restore original stat (protects pytest teardown)
    Path.stat = original_stat

    assert len(eligible) == 2
    expected_total = 2 if exclude_patterns else 3
    expected_total_size = 3000 if exclude_patterns else 3500
    assert summary["total_files"] == expected_total
    assert summary["total_size"] == expected_total_size
