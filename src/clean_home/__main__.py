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
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulate or perform cleanup of large/old files."
    )
    parser.add_argument("-path", type=Path,
                        default=Path.home(), help=f"Folder to scan (default: {Path.home()}")
    parser.add_argument("-min-size-mb", type=int, default=0,
                        help="Minimum file size in MB")
    parser.add_argument("-older-than-days", type=int,
                        default=0, help="Older than X days")
    parser.add_argument("-move-to", type=Path, default="~/cleaned",
                        help="Destination directory")
    parser.add_argument("-exclude", action="append",
                        default=[], help="Exclude pattern(s)")
    parser.add_argument("-really", action="store_true",
                        help="Actually move files")
    parser.add_argument("-v", "--verbose", action="count",
                        default=0, help="Increase verbosity (-v, -vv)")

    return parser.parse_args()


def main():
    args = parse_args()

    # --- Validation ---
    if not args.path.is_dir():
        logging.error(f"Error: Path is not a valid directory: {args.path}")
        return

    if args.really and not args.move_to:
        logging.error(
            "Error: The '-move-to' argument is required when using '-really'.")
        return

    root = Path(args.path).expanduser()
    move_to = Path(args.move_to).expanduser()
    # print(root)
    # logging.info("Scanning %s", root)


if __name__ == "__main__":
    main()
