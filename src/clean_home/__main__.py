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
