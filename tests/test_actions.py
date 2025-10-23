from clean_home.actions import perform_actions
from unittest.mock import patch
from pathlib import Path
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
