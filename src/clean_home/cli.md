# CLI Draft (Arg Names & Help)

--path PATH               Directory to scan (default: user home)
--min-size-mb INT         Min file size in MB (default: 50)
--older-than-days INT     Min age in days (default: 90)
--move-to PATH            Destination (created if missing)
--exclude PATTERN         Glob to ignore (repeatable)
--really                  Actually move files
--format human|json       Output format (default: human)

Exit codes:
0 = OK; 1 = thresholds exceeded but no action; 2 = invalid input; 3 = runtime error
