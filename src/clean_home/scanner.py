# TODO: Implement filesystem scan (read-only).
# - Use pathlib.Path.rglob("*") or os.walk
# - Collect FileInfo dicts
# - Mark hidden files/dirs (name startswith ".")
# - Handle permission errors (try/except, log + continue)
#
# def scan(root_path: str) -> list[dict]:
#     """Return list of FileInfo dicts (no filtering)."""
#     ...
