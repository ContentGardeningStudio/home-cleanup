# Home Cleanup Dry-Run

> CLI that scans a directory and **simulates** cleanup (dry-run by default).
> Moves files only if `--really` is passed.

## Objectives
- Practice `os`, `pathlib`, `argparse`, `logging`.
- Separate pure logic (scan, filter, summarize) from side effects (moves).

## CLI (target)
- `--path PATH` (default: home)
- `--min-size-mb INT` (default: 50)
- `--older-than-days INT` (default: 90)
- `--move-to PATH` (default: ./_quarantine)
- `--exclude PATTERN` (repeatable; e.g., `--exclude "*.log"`)
- `--really` (perform moves)
- `--format human|json` (default: human)

## Getting Started
- [ ] Create virtual env
- [ ] Install deps (`pip install -e .` once defined)
- [ ] Run: `python -m clean_home --help` (after implementing)

## Architecture (high level)
- `scanner.py` → walk filesystem, collect `FileInfo` dicts
- `filters.py` → pure functions to decide "candidate?"
- `summarize.py` → counts, total sizes
- `actions.py` → dry-run log vs. real move
- `logging_conf.py` → logging setup
- `__main__.py` → argument parsing + orchestration

## Acceptance Criteria
- [ ] Dry-run prints actions, no changes by default
- [ ] Real run creates `--move-to` if missing and moves candidates
- [ ] Respect excludes + denylist (e.g., `.git`, `node_modules`)
- [ ] Clear summary at end (counts + size)
- [ ] Graceful errors (permissions, missing paths)

## Stretch (optional)
- [ ] Glob patterns for excludes and subpaths
- [ ] Progress indicator (simple % on stdout)
- [ ] JSON output for scripting
