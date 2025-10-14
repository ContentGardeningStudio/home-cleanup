# TODO: Pure filtering rules.
# def is_candidate(fileinfo, min_size_mb, older_than_days, excludes) -> bool: ...
# Helper ideas:
# - size_in_mb = fileinfo["size_bytes"] / (1024*1024)
# - age_days = (now_ts - fileinfo["mtime_ts"]) / 86400
# - match excludes via fnmatch.fnmatch(fileinfo["path"], pattern)
#
# Keep deterministic + testable.
