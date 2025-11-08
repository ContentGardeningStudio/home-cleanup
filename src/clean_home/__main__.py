# TODO: Parse CLI args and orchestrate calls.
# Suggested steps:
# 1) parse_args()  -> dict
# 2) files = scan(path)
# 3) candidates = apply_filters(files, thresholds, excludes)
# 4) stats = summarize(candidates)
# 5) if really: perform_moves(candidates, move_to)
# 6) print_report(stats, format)
#
# NOTE: keep functions small; avoid side effects in helpers.

import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from . import scanner, actions
from .logging_conf import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate or perform cleanup of large/old files."
    )
    parser.add_argument(
        "-path",
        type=Path,
        default=Path.cwd(),
        help=f"Folder to scan (default: {Path.cwd()})",
    )
    parser.add_argument(
        "-min-size-mb", type=int, default=90, help="Minimum file size in MB"
    )
    parser.add_argument(
        "-older-than-days", type=int, default=90, help="Older than X days"
    )
    parser.add_argument(
        "-move-to", type=Path, default="~/_quarantine", help="Destination directory"
    )
    parser.add_argument(
        "-exclude", action="append", default=[], help="Exclude pattern(s)"
    )
    parser.add_argument("-really", action="store_true", help="Actually move files")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    setup_logging(args.verbose)

    logging.info("App starting: Initializing arguments.")

    # --- Validation of arguments ---
    if not args.path.is_dir():
        logging.error(f" Path is not a valid directory: {args.path}")
        return

    if args.really and not args.move_to:
        logging.error(" The '-move-to' argument is required when using '-really'.")
        return

    # Calculate the cutoff timestamp
    cutoff_time = datetime.now() - timedelta(days=args.older_than_days)

    logging.info(f"Starting scan in: {args.path}")
    logging.info(
        f"Criteria: > {args.min_size_mb}MB and older than {args.older_than_days} days."
    )

    # call the scanner module
    eligible_files, summary = scanner.scan_directory(
        root_dir=args.path,
        min_size_bytes=args.min_size_mb * 1024 * 1024,
        cutoff_time=cutoff_time,
        exclude_patterns=args.exclude,
    )

    print("\n--- Scan Summary ---")
    print(f"Total files found: {summary['total_files']:,}")
    print(f"Total size found: {summary['total_size'] / (1024 * 1024 * 1024):.2f} GB")
    print(f"Files eligible for action: {len(eligible_files):,}")
    print(
        f"Total size of eligible files: {sum(f.stat().st_size for f in eligible_files) / (1024 * 1024 * 1024):.2f} GB"
    )
    print(f"Mode: {'REAL ACTION' if args.really else 'DRY-RUN'}")
    print(f"Move Target: {args.move_to or 'N/A'}")
    print("--------------------\n")

    if eligible_files:
        actions.perform_actions(
            eligible_files=eligible_files,
            move_target=args.move_to,
            is_dry_run=not args.really,
        )
    else:
        logging.info("No files found that match the criteria.")


if __name__ == "__main__":
    main()
