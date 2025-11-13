from clean_home.actions import perform_actions
from unittest.mock import patch
import logging

# let logging be in a quietmode
logging.basicConfig(level=logging.CRITICAL)


def test_dry_run_no_move(move_setup):
    """Test that in dry-run mode, files are NOT moved and destination is NOT created."""
    eligible_files, move_to_dir, source_dir = move_setup

    perform_actions(eligible_files, move_to_dir, is_dry_run=True)

    # Check that the files still exist in the source directory
    for f in eligible_files:
        assert f.exists()

    # Check that the destination directory was NOT created
    assert not move_to_dir.exists()


def test_real_move_success(move_setup):
    """Test that in real mode, files are moved successfully."""
    eligible_files, move_to_dir, source_dir = move_setup

    perform_actions(eligible_files, move_to_dir, is_dry_run=False)

    # Check that the destination directory was created
    assert move_to_dir.is_dir()

    # Check files are GONE from the source and EXIST in the destination
    for f in eligible_files:
        assert not f.exists()
        assert (move_to_dir / f.name).exists()


def test_real_move_failure_handling(move_setup):
    """Test that an OSError during move is handled gracefully and the program continues."""
    eligible_files, move_to_dir, source_dir = move_setup

    # Patch shutil.move to fail on the first file, but succeed on the second (by passing)
    with patch("shutil.move") as mock_move:
        # Side effect sequence: Error on first call, then pass (return None)
        mock_move.side_effect = [OSError("Test: Disk full"), None]

        # Act: This should attempt two moves and log one failure
        summary = perform_actions(eligible_files, move_to_dir, is_dry_run=False)

    # 1. Ensure the move was attempted for ALL eligible files
    assert mock_move.call_count == len(eligible_files)
    # 2. Ensure the summary reflects the failure and success
    assert summary["files_failed"] == 1
    assert summary["files_moved"] == 1
