# TODO: Side effects (dry-run vs. real).
# def plan_moves(candidates, move_to) -> list[tuple[src, dst]]  # pure
# def perform_moves(plan) -> list[tuple[src, dst, ok_bool, error_str]]  # impure
#
# Create move_to if missing.
# Use shutil.move; ensure same-device vs cross-device moves handled by shutil.
import logging
import shutil
from pathlib import Path


def perform_actions(eligible_files: list[Path], move_target: Path, is_dry_run: bool):
    """Logs actions in dry-run or performs actual file moves."""

    if is_dry_run:
        logging.info(
            "\n*** DRY-RUN: Listing actions that would be performed: ***")
        for file in eligible_files:
            size_mb = file.stat().st_size / (1024 * 1024)
            logging.info(
                f"[DRY-RUN] Would move {file} (Size: {size_mb:.2f} MB) to {move_target}")
        logging.info(
            "*** DRY-RUN Complete. To perform action, re-run with -really. ***")
        return

    # --- Real Action ---
    logging.info(
        f"\n*** REAL ACTION: Moving {len(eligible_files)} files to {move_target} ***")

    # Ensure the target directory exists (Constraint: create if missing)
    try:
        move_target.mkdir(parents=True, exist_ok=True)
        logging.info(f"Target directory ensured: {move_target}")
    except Exception as e:
        logging.error(f"Failed to create target directory {move_target}: {e}")
        return

    success_count = 0
    fail_count = 0

    for file in eligible_files:
        try:
            # Construct new path
            destination = move_target / file.name

            # Constraint: Use shutil.move
            shutil.move(str(file), str(destination))

            logging.info(f"[SUCCESS] Moved: {file.name} -> {destination}")
            success_count += 1

        except Exception as e:
            logging.error(f"[ERROR] Failed to move {file}: {e}")
            fail_count += 1

    logging.info(f"\n*** ACTION COMPLETE ***")
    logging.info(f"Successfully moved: {success_count}")
    # Use error level for visibility
    logging.error(f"Failed to move: {fail_count}")
    return {'files_moved': success_count, "files_failed": fail_count}
