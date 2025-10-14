# Design

## Goals
- Predictable dry-run by default; no surprise deletions.
- Pure logic testable without touching the filesystem.

## Data Model (sketch)
- FileInfo (dict):
  - path: str
  - size_bytes: int
  - mtime_ts: float
  - is_hidden: bool

## Control Flow
1. Parse args → config dict
2. `scan(path)` → list[FileInfo]
3. `apply_filters(files, rules)` → candidates
4. `summarize(candidates)` → counts/size
5. If `--really`: `perform_moves(candidates, move_to)`
6. Print summary (human or JSON)

## Error Handling
- Missing directory → exit code 2
- Permission errors → warn, skip
- Partial failures → collect and report
