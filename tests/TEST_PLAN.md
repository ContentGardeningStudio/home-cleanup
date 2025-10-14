# Test Plan (No code)

## Unit (pure)
- filters.is_candidate: size/age/excludes combinations
- summarize.summarize: counts and totals

## Integration (no destructive ops)
- scanner.scan on sample_data
- actions.plan_moves (pure)

## E2E (safe)
- Dry-run end-to-end prints expected actions
- Real run moves to `_quarantine/` inside a temp dir

## Edge Cases
- Permission denied on subdir
- Broken symlink
- Very long paths
- Non-UTF8 filenames (print safely)
