# Backup Integrity Tool

Backup Integrity Tool is a Python command-line application that checks whether a backup directory is consistent with a source directory.

It compares files recursively using relative paths and SHA256 hashes. The tool can detect which files are identical, missing from the backup, extra in the backup, or modified.

# Current status

Work in progress.

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
- Basic pytest tests for hash calculation, file scanning, and directory comparison.

Planned features:

- Terminal report generation.
- Optional report saving.
- Dry-run mode.
- Optional backup creation/update mode.

## Technologies

- Python
- pathlib
- hashlib
- pytest