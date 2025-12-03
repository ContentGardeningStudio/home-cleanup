<h1 align="center">🧹 Home Cleanup CLI</h1>
<p align="center">
  Smart file cleanup for your home directory — <strong>safe by default</strong> (dry-run mode).  
  <br/>
  Move, quarantine, or summarize large / old files with confidence.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square" />
  <img src="https://img.shields.io/github/license/ContentGardeningStudio/home-cleanup?style=flat-square&color=green" />
  <img src="https://img.shields.io/github/stars/ContentGardeningStudio/home-cleanup?style=flat-square&color=yellow" />
</p>

---

## 🧭 Overview

**Home Cleanup** is a command-line tool that scans your filesystem and identifies large or old files for potential cleanup.  
By default, it runs in **dry-run mode** — simulating what would happen before any files are actually moved.  

When you’re confident, just add the `--really` flag to perform the moves.

> ⚙️ Ideal for developers, sysadmins, or power users who want to declutter large directories safely.


## ⚙️ Quickstart

```bash
git clone https://github.com/ContentGardeningStudio/home-cleanup
cd home-cleanup
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -e .
python -m clean_home --help
```


## 🧰 CLI Usage

```bash
python -m clean_home --path ~/Downloads --older-than-days 90 --min-size-mb 50
```

| Flag | Description | Default |
|------|--------------|----------|
| `--path PATH` | Target directory to scan | `~/` |
| `--min-size-mb INT` | Minimum file size | `50 MB` |
| `--older-than-days INT` | Minimum file age | `90 days` |
| `--move-to PATH` | Destination for moved files | `./_quarantine` |
| `--exclude PATTERN` | Glob pattern to exclude (repeatable) | `None` |
| `--really` | Perform actual move (disable dry-run) | Off |
| `--format human|json` | Output format | `human` |


## 🧩 Architecture

```
clean_home/
 ┣ 📄 __main__.py
 ┣ 📄 scanner.py
 ┣ 📄 filters.py
 ┣ 📄 summarize.py
 ┣ 📄 actions.py
 ┗ 📄 logging_conf.py
```


## 📊 Output Examples

### Human Format
```
Found 12 candidates (1.2 GB total)
  /Users/alex/Downloads/old_backup.zip (600 MB, 180 days old)
  /Users/alex/Movies/recording.mov (420 MB, 270 days old)
Dry-run only — no files were moved.
```

### JSON Format
```json
{
  "candidates": 12,
  "total_size_mb": 1200,
  "files": [
    {"path": "...", "size_mb": 600, "days_old": 180}
  ]
}
```


## 🧠 Learning Objectives

- Practice Python’s standard libs: `os`, `pathlib`, `argparse`, `logging`
- Separate pure logic from side effects
- Implement safe dry-run vs real mode


## 🤝 Contributing

Pull requests and ideas welcome!

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/new-filter`)  
3. Commit your changes  
4. Open a PR 🚀  


## 🔗 Join Our Skool Community

We help MVP builders ship better. Join our Skool community for feedback, technical guidance, and deep-dive discussions to level up your project.

👉 Join here: https://www.skool.com/onboard-or-join-a-tech-team


## 📜 License

Licensed under the [MIT License](LICENSE).  
© 2025 [Content Gardening Studio](https://github.com/ContentGardeningStudio) — small, focused tools for modern dev workflows.
