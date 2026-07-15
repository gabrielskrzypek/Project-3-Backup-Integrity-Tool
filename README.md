# Backup Integrity Tool

Backup Integrity Tool is a Python command-line application that checks whether a backup directory is consistent with a source directory.

It compares files recursively using relative paths and SHA256 hashes. The tool can detect which files are identical, missing from the backup, extra in the backup, or modified.

Currently implemented:

- Initial project structure.
- SHA256 hash calculation for individual files.
- Recursive file scanning.
- File hash collection using relative paths.
- Source and backup directory comparison.
- Detection of:
  - identical files,
  - files missing from backup,
  - extra files in backup,
  - modified files.
- Text report generation with:
  - source and backup paths,
  - summary counts,
  - detailed file lists,
  - `None` for empty categories.
- Pytest tests for hash calculation, recursive scanning, directory comparison, and report generation.

Planned features:

- CLI arguments with `argparse`.
- Path validation and error handling.
- Optional report saving.
- Dry-run mode.
- Optional backup creation and update mode.
- Safe overwrite control.

## Technologies

- Python
- pathlib
- hashlib
- pytest