# Backup Integrity Tool

Backup Integrity Tool is a Python command-line application that checks whether a backup directory is consistent with a source directory.

It compares files recursively using relative paths and SHA256 hashes. The tool can detect which files are identical, missing from the backup, extra in the backup, or modified.

# Currently implemented:

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
- Text report generation.
- Optional report saving with timestamped filenames.
- Custom output directory with `--output`.
- `--no-save` mode.
- Command-line arguments with `argparse`.
- Source and backup path validation.
- Pytest tests for:
  - hash calculation,
  - recursive scanning,
  - directory comparison,
  - report generation,
  - path validation.

# Planned features:

- Dry-run mode.
- Optional backup creation and update mode.
- Safe overwrite control.
- Final clean test from a fresh clone.

## Technologies

- Python
- pathlib
- hashlib
- pytest