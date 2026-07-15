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
- Optional backup creation with `--create-backup`.
- Copying of files missing from the backup.
- Automatic creation of missing subdirectories.
- Optional overwrite of modified backup files with `--overwrite`.
- `--dry-run` mode for previewing copy and overwrite actions.
- Verification after backup updates.
- 18 pytest tests covering:
  - hash calculation,
  - recursive scanning,
  - directory comparison,
  - report generation,
  - path validation,
  - missing-file copying,
  - subdirectory creation,
  - overwrite behavior,
  - dry-run behavior.

# Planned features:

- Validation of incompatible CLI argument combinations.
- Optional handling of extra backup files.
- Final README usage examples.
- Clean installation and execution test from a fresh clone.

## Technologies

- Python
- pathlib
- hashlib
- pytest